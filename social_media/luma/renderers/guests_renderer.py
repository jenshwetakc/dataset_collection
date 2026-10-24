from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.common.media_generator import ASSETS_ROOT

from social_media.luma.generators.guests_generator import (
    GUEST_STATES,
    apply_guests_state,
    generate_guests_data,
)
from social_media.luma.renderers.common_renderer import render_page

LUMA_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = LUMA_ROOT / "templates"
OUTPUT_ROOT = LUMA_ROOT / "output"

AVATARS_DIR = ASSETS_ROOT  / "avatars"

NUM_SAMPLES = 7

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


async def render_guest_job(
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
        try:
            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"guests_{page_data['state']}",
                template_name="guests.html",
                context_key="discover",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="guests",
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
                "[LUMA GUESTS FAILED] "
                f"sample={sample_index} "
                f"state={page_data['state']} "
                f"viewport={viewport['name']} "
                f"error={error!r}"
            )
            return {"status": "failed", "error": repr(error)}


async def main(browser):
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    successful = 0
    failed = 0

    for sample_index in range(NUM_SAMPLES):
        page_data = apply_guests_state(
            generate_guests_data(
                sample_index=sample_index,
                avatars_dir=AVATARS_DIR,
            ),
            random.choice(GUEST_STATES),
        )

        mode = (
            random.choice(["light", "dark"])
            if THEME_MODE == "random"
            else THEME_MODE
        )
        theme = generate_accessible_theme(mode=mode)

        print(
            "[LUMA GUESTS] "
            f"sample={sample_index} "
            f"state={page_data['state']} theme={mode}"
        )

        results = await asyncio.gather(*[
            render_guest_job(
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
        ])

        successful += sum(
            result["status"] == "success" for result in results
        )
        failed += sum(
            result["status"] == "failed" for result in results
        )

    print(
        "[LUMA GUESTS COMPLETE] "
        f"successful={successful} failed={failed}"
    )

    if failed:
        raise RuntimeError(
            f"{failed} guest renders failed. See failure messages."
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