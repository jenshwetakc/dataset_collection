from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.pycharm.generators.welcome_generator import (
    WELCOME_STATES,
    generate_welcome_data,
)
from social_media.pycharm.renderers.common_renderer import render_pycharm_page


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 20

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

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

# The welcome screen does not need document-scroll captures.
SCROLL_PERCENTAGES = [0]

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
# Render Job
# ==========================================================

async def render_one_welcome_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    welcome_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[PYCHARM WELCOME]",
                "sample=",
                sample_index,
                "state=",
                state,
                "viewport=",
                viewport["name"],
                "theme=",
                theme["mode"],
            )

            await render_pycharm_page(
                browser=browser,
                sample_index=sample_index,
                page_type="welcome",
                template_name="welcome.html",
                context_key="welcome",
                page_data=welcome_data,
                system=system,
                theme=theme,
                viewport=viewport,
                # All welcome states stay in this one output folder.
                output_subdir="welcome",
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
                "[PYCHARM WELCOME FAILED]",
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
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    sample_index = 0

    for state in WELCOME_STATES:
        for _ in range(NUM_SAMPLES_PER_STATE):
            welcome_data = generate_welcome_data(state=state)
            system = generate_system_data()
            theme = generate_theme()

            for viewport in viewports:
                jobs.append(
                    render_one_welcome_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        state=state,
                        welcome_data=welcome_data,
                        system=system,
                        theme=theme,
                        viewport=viewport,
                    )
                )

            sample_index += 1

    results = await asyncio.gather(*jobs)

    successful = sum(
        result["status"] == "success"
        for result in results
    )
    failed = len(results) - successful

    print(
        "\n[PYCHARM WELCOME COMPLETE]",
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