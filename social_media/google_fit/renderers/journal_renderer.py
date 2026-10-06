from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.system_generator import (
    generate_system_data,
)
from social_media.common.viewport import (
    get_all_viewports,
    get_random_viewport,
    get_viewports_by_category,
    get_viewports_by_names,
    get_viewports_by_size_class,
)
from social_media.google_fit.generators.journal_generator import (
    generate_journal_data,
)
from social_media.google_fit.renderers.common_renderer import (
    render_google_fit_page,
)

# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 20

VIEWPORT_MODE = "selected"

SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_android",
    "standard_iphone",
    "large_mobile",
    "mobile_landscape",
    "tablet_portrait",
    "large_tablet_portrait",
    "tablet_landscape",
    "foldable",
    "small_laptop",
    "laptop",
    "large_laptop",
    "desktop_fhd",
    "desktop_qhd",
    "desktop_4k",
    "ultrawide",
]

# light | dark | random | both
THEME_MODE = "random"

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MIN_VISIBLE_RATIO = 0.20
MIN_SCROLL_DELTA = 100
SCROLL_SETTLE_MS = 150

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Viewports
# ==========================================================

def resolve_selected_viewports() -> list[dict]:
    if VIEWPORT_MODE == "all":
        return get_all_viewports()

    if VIEWPORT_MODE == "selected":
        return get_viewports_by_names(
            SELECTED_VIEWPORTS
        )

    if VIEWPORT_MODE == "random":
        return [get_random_viewport()]

    if VIEWPORT_MODE in {
        "mobile",
        "mobile_landscape",
        "tablet",
        "foldable",
        "laptop",
        "desktop",
        "ultrawide",
    }:
        return get_viewports_by_category(
            VIEWPORT_MODE
        )

    if VIEWPORT_MODE in {
        "compact",
        "medium",
        "expanded",
    }:
        return get_viewports_by_size_class(
            VIEWPORT_MODE
        )

    raise ValueError(
        f"Unknown VIEWPORT_MODE: {VIEWPORT_MODE}"
    )


# ==========================================================
# Theme
# ==========================================================

def resolve_theme_modes() -> list[str]:
    if THEME_MODE == "both":
        return [
            "light",
            "dark",
        ]

    if THEME_MODE == "random":
        return [
            random.choice(["light", "dark"])
        ]

    if THEME_MODE in {"light", "dark"}:
        return [THEME_MODE]

    raise ValueError(
        f"Unknown THEME_MODE: {THEME_MODE}"
    )


# ==========================================================
# Render Job
# ==========================================================

async def render_journal_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    journal_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[GOOGLE FIT JOURNAL]",
                "sample=",
                sample_index,
                "theme=",
                theme["mode"],
                "viewport=",
                viewport["name"],
            )

            await render_google_fit_page(
                browser=browser,
                sample_index=sample_index,
                page_type="journal",
                template_name="journal.html",
                context_key="journal",
                page_data=journal_data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="journal",
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=MIN_VISIBLE_RATIO,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
                min_scroll_delta=MIN_SCROLL_DELTA,
                scroll_settle_ms=SCROLL_SETTLE_MS,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[GOOGLE FIT JOURNAL FAILED]",
                "sample=",
                sample_index,
                "viewport=",
                viewport["name"],
                "error=",
                error,
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    viewports = resolve_selected_viewports()
    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )
    jobs = []

    for sample_index in range(NUM_SAMPLES):
        journal_data = generate_journal_data()

        for theme_mode in resolve_theme_modes():
            theme = generate_accessible_theme(
                mode=theme_mode
            )
            system = generate_system_data()

            for viewport in viewports:
                jobs.append(
                    render_journal_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        journal_data=journal_data,
                        system=system,
                        theme=theme,
                        viewport=viewport,
                    )
                )

    results = await asyncio.gather(*jobs)

    successful = sum(
        result["status"] == "success"
        for result in results
    )
    failed = len(results) - successful

    print(
        "[GOOGLE FIT JOURNAL COMPLETE]",
        "successful=",
        successful,
        "failed=",
        failed,
    )


# ==========================================================
# Entry Point
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True
        )

        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())