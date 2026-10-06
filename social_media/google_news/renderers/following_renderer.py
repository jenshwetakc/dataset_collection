from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.google_news.generators.following_generator import (
    FOLLOWING_STATES,
    generate_following_data,
)
from social_media.google_news.renderers.common_renderer import (
    render_google_news_page,
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

THEME_MODE = "random"

# "random", "cycle", "selected", or a state from FOLLOWING_STATES.
STATE_MODE = "cycle"

SELECTED_STATES = [
    "normal",
    "topic_focus",
    "manage",
    "source_grid",
    "unfollow_dialog",
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

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(mode=mode)


# ==========================================================
# State Resolver
# ==========================================================

def get_state(sample_index: int) -> str | None:
    if STATE_MODE == "random":
        return None

    if STATE_MODE == "cycle":
        return FOLLOWING_STATES[
            sample_index % len(FOLLOWING_STATES)
        ]

    if STATE_MODE == "selected":
        return random.choice(SELECTED_STATES)

    if STATE_MODE in FOLLOWING_STATES:
        return STATE_MODE

    raise ValueError(
        f"Unknown STATE_MODE: {STATE_MODE}"
    )


# ==========================================================
# Render Job
# ==========================================================

async def render_one_following_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    page_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[GOOGLE NEWS FOLLOWING]",
                "sample=",
                sample_index,
                "state=",
                page_data["state"],
                "viewport=",
                viewport["name"],
                "theme=",
                theme["mode"],
            )

            await render_google_news_page(
                browser=browser,
                sample_index=sample_index,
                page_type="following",
                template_name="following.html",
                context_key="following",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                # All states are saved under one directory.
                output_subdir="following",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": page_data["state"],
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[GOOGLE NEWS FOLLOWING FAILED]",
                "sample=",
                sample_index,
                "state=",
                page_data["state"],
                "viewport=",
                viewport["name"],
                "error=",
                error,
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": page_data["state"],
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    for sample_index in range(NUM_SAMPLES):
        page_data = generate_following_data(
            state=get_state(sample_index),
        )
        system = generate_system_data()
        theme = generate_theme()

        for viewport in viewports:
            jobs.append(
                render_one_following_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    page_data=page_data,
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
        "\n[GOOGLE NEWS FOLLOWING COMPLETE]",
        f"successful={successful}",
        f"failed={failed}",
    )


# ==========================================================
# Entry Point
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())