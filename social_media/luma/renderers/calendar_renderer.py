from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

from social_media.luma.generators.calendar_generator import (
    CALENDAR_STATES,
    apply_calendar_state,
    generate_calendar_data,
)
from social_media.luma.renderers.common_renderer import render_page

LUMA_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = LUMA_ROOT / "templates"
OUTPUT_ROOT = LUMA_ROOT / "output"

NUM_SAMPLES = 5

SELECTED_VIEWPORTS = [
    "small_mobile",
    # "standard_android",
    # "standard_iphone",
    # "large_mobile",
    # "mobile_landscape",
    # "tablet_portrait",
    # "large_tablet_portrait",
    # "tablet_landscape",
    # "foldable",
    # "small_laptop",
    # "laptop",
    # "large_laptop",
    # "desktop_fhd",
    # "desktop_qhd",
    # "desktop_4k",
    "ultrawide",
]

ANNOTATION_PROFILES = ["big_components", "small_elements"]

THEME_MODE = "random"
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
SAVE_VISUALIZATIONS = True
MAX_CONCURRENT_WORKERS = 4


def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )
    return generate_accessible_theme(mode=mode)


async def render_calendar_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    calendar: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = calendar["state"]

        try:
            print(
                "[LUMA CALENDAR] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"calendar_{state}",
                template_name="calendar.html",
                context_key="discover",
                page_data=calendar,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="calendar",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0] if calendar["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {"status": "success"}

        except Exception as error:
            print(
                "[LUMA CALENDAR FAILED] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"error={error!r}"
            )
            return {
                "status": "failed",
                "error": repr(error),
            }


async def main(browser) -> None:
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    for sample_index in range(NUM_SAMPLES):
        base_data = generate_calendar_data(
            sample_index=sample_index,
        )

        calendar = apply_calendar_state(
            base_data,
            random.choice(CALENDAR_STATES),
        )

        theme = generate_theme()

        for viewport in viewports:
            system = generate_system_data(
                style="random",
                icon_density="random",
                viewport=viewport,
            )

            jobs.append(
                render_calendar_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    calendar=calendar,
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
        "[LUMA CALENDAR COMPLETE] "
        f"successful={successful} failed={failed}"
    )

    if failed:
        raise RuntimeError(
            f"{failed} calendar renders failed. "
            "See [LUMA CALENDAR FAILED] messages above."
        )


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())