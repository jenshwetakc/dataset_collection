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
    get_viewports_by_names,
)
from social_media.google_fit.generators.browse_generator import (
    BROWSE_STATES,
    generate_browse_data,
)
from social_media.google_fit.renderers.common_renderer import (
    render_google_fit_page,
)

# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 20

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

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

# random | all | selected
STATE_MODE = "random"

SELECTED_STATES = [
    "default",
    "search_active",
    "offline",
]

# light | dark | both | random
THEME_MODE = "random"

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# State Resolver
# ==========================================================

def resolve_states() -> list[str]:
    if STATE_MODE == "random":
        return [
            random.choice(BROWSE_STATES)
        ]

    if STATE_MODE == "all":
        return list(BROWSE_STATES)

    if STATE_MODE == "selected":
        invalid = (
            set(SELECTED_STATES)
            - set(BROWSE_STATES)
        )

        if invalid:
            raise ValueError(
                f"Unknown browse states: {sorted(invalid)}"
            )

        return list(SELECTED_STATES)

    raise ValueError(
        f"Unknown STATE_MODE: {STATE_MODE}"
    )


# ==========================================================
# Theme Resolver
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

async def render_browse_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    browse_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[GOOGLE FIT BROWSE]",
                "sample=",
                sample_index,
                "state=",
                state,
                "theme=",
                theme["mode"],
                "viewport=",
                viewport["name"],
            )

            await render_google_fit_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"browse_{state}",
                template_name="browse.html",
                context_key="browse",
                page_data=browse_data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="browse",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[GOOGLE FIT BROWSE FAILED]",
                "sample=",
                sample_index,
                "state=",
                state,
                "viewport=",
                viewport["name"],
                "error=",
                error,
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )
    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )
    jobs = []

    for sample_index in range(NUM_SAMPLES):
        for state in resolve_states():
            browse_data = generate_browse_data(
                state=state
            )

            for theme_mode in resolve_theme_modes():
                theme = generate_accessible_theme(
                    mode=theme_mode
                )
                system = generate_system_data()

                for viewport in viewports:
                    jobs.append(
                        render_browse_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            state=state,
                            browse_data=browse_data,
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
        "[GOOGLE FIT BROWSE COMPLETE]",
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