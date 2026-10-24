from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

from social_media.luma.generators.my_events_generator import (
    MY_EVENTS_STATES,
    apply_my_events_state,
    generate_my_events_data,
)
from social_media.luma.renderers.common_renderer import render_page

LUMA_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = LUMA_ROOT / "templates"
OUTPUT_ROOT = LUMA_ROOT / "output"

NUM_SAMPLES = 5

SELECTED_VIEWPORTS = [
    "small_mobile",
    # "standard_android", "standard_iphone",
    # "large_mobile", "mobile_landscape", "tablet_portrait",
    # "large_tablet_portrait", "tablet_landscape", "foldable",
    # "small_laptop", "laptop", "large_laptop",
    # "desktop_fhd", "desktop_qhd", "desktop_4k",
    "ultrawide",
]

ANNOTATION_PROFILES = ["big_components", "small_elements"]
THEME_MODE = "random"
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
SAVE_VISUALIZATIONS = True
MAX_CONCURRENT_WORKERS = 4


async def render_job(
    *,
    browser,
    semaphore,
    sample_index,
    page_data,
    system,
    theme,
    viewport,
):
    async with semaphore:
        state = page_data["state"]

        try:
            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"my_events_{state}",
                template_name="my_events.html",
                context_key="discover",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="my_events",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0] if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )
            return {"status": "success"}

        except Exception as error:
            print(
                "[LUMA MY EVENTS FAILED] "
                f"sample={sample_index} state={state} "
                f"viewport={viewport['name']} error={error!r}"
            )
            return {"status": "failed", "error": repr(error)}


async def main(browser):
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    successful = 0
    failed = 0

    for sample_index in range(NUM_SAMPLES):
        page_data = apply_my_events_state(
            generate_my_events_data(sample_index=sample_index),
            random.choice(MY_EVENTS_STATES),
        )

        mode = (
            random.choice(["light", "dark"])
            if THEME_MODE == "random"
            else THEME_MODE
        )
        theme = generate_accessible_theme(mode=mode)

        print(
            "[LUMA MY EVENTS] "
            f"sample={sample_index} state={page_data['state']} "
            f"theme={mode}"
        )

        jobs = [
            render_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                page_data=page_data,
                system=generate_system_data(
                    style="random",
                    icon_density="random",
                    viewport=viewport,
                ),
                theme=theme,
                viewport=viewport,
            )
            for viewport in viewports
        ]

        # Keep only one sample's image data in flight.
        results = await asyncio.gather(*jobs)

        successful += sum(
            result["status"] == "success"
            for result in results
        )
        failed += sum(
            result["status"] == "failed"
            for result in results
        )

    print(
        "[LUMA MY EVENTS COMPLETE] "
        f"successful={successful} failed={failed}"
    )

    if failed:
        raise RuntimeError(
            f"{failed} My Events renders failed. See messages above."
        )


async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())