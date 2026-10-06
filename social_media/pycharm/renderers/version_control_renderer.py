from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.pycharm.generators.version_control_generator import (
    VERSION_CONTROL_STATES,
    generate_version_control_data,
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

# IDE layouts do not naturally document-scroll.
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

async def render_one_version_control_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    vcs_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[PYCHARM VERSION CONTROL]",
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
                page_type="version_control",
                template_name="version_control.html",
                context_key="vcs",
                page_data=vcs_data,
                system=system,
                theme=theme,
                viewport=viewport,
                # Every state is saved in one directory.
                output_subdir="version_control",
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
                "[PYCHARM VERSION CONTROL FAILED]",
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

    for state in VERSION_CONTROL_STATES:
        for _ in range(NUM_SAMPLES_PER_STATE):
            vcs_data = generate_version_control_data(state=state)
            system = generate_system_data()
            theme = generate_theme()

            for viewport in viewports:
                jobs.append(
                    render_one_version_control_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        state=state,
                        vcs_data=vcs_data,
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
        "\n[PYCHARM VERSION CONTROL COMPLETE]",
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