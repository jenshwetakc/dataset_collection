from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.pycharm.generators.tool_window_generator import (
    TOOL_WINDOW_STATES,
    generate_tool_window_data,
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

# IDE layouts do not use document scrolling.
SCROLL_PERCENTAGES = [0]

# True = right/side panel visible; False = collapsed.
PANEL_STATES = [
    True,
    False,
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
# Render Job
# ==========================================================

async def render_one_tool_window_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    panel_open: bool,
    workspace_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    panel_label = "open" if panel_open else "closed"

    async with semaphore:
        try:
            print(
                "[PYCHARM TOOL WINDOW]",
                "sample=",
                sample_index,
                "state=",
                state,
                "panel=",
                panel_label,
                "viewport=",
                viewport["name"],
                "theme=",
                theme["mode"],
            )

            await render_pycharm_page(
                browser=browser,
                sample_index=sample_index,
                page_type="tool_window",
                template_name="tool_window.html",
                context_key="workspace",
                page_data=workspace_data,
                system=system,
                theme=theme,
                viewport=viewport,
                # All UI states stay in one output directory.
                output_subdir="tool_window",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": state,
                "panel": panel_label,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[PYCHARM TOOL WINDOW FAILED]",
                "sample=",
                sample_index,
                "state=",
                state,
                "panel=",
                panel_label,
                "viewport=",
                viewport["name"],
                "error=",
                error,
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": state,
                "panel": panel_label,
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

    for state in TOOL_WINDOW_STATES:
        for panel_open in PANEL_STATES:
            for _ in range(NUM_SAMPLES_PER_STATE):
                workspace_data = generate_tool_window_data(
                    state=state,
                    panel_open=panel_open,
                )
                system = generate_system_data()
                theme = generate_theme()

                for viewport in viewports:
                    jobs.append(
                        render_one_tool_window_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            state=state,
                            panel_open=panel_open,
                            workspace_data=workspace_data,
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
        "\n[PYCHARM TOOL WINDOW COMPLETE]",
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