from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.media_generator import ASSETS_ROOT
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

from social_media.tinypal.generators.history_generator import (
    HISTORY_STATES,
    apply_history_state,
    generate_history_data,
)
from social_media.tinypal.renderers.common_renderer import render_page


TINYPAL_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = TINYPAL_ROOT / "templates"
OUTPUT_ROOT = TINYPAL_ROOT / "output"
AVATARS_DIR = ASSETS_ROOT / "tinypal"

NUM_SAMPLES = 8

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
SAVE_VISUALIZATIONS = True

SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
MAX_CONCURRENT_WORKERS = 4


async def render_history_job(
    *,
    browser,
    semaphore,
    sample_index,
    page_data,
    system,
    theme,
    viewport,
) -> dict:
    async with semaphore:
        state = page_data["state"]

        try:
            print(
                f"[TINYPAL HISTORY] sample={sample_index} "
                f"state={state} viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"history_{state}",
                template_name="history.html",
                context_key="tinypal",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="history",
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=0.20,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0] if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                "status": "success",
                "state": state,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[TINYPAL HISTORY FAILED] sample={sample_index} "
                f"state={state} viewport={viewport['name']} "
                f"error={error!r}"
            )

            return {
                "status": "failed",
                "state": state,
                "viewport": viewport["name"],
                "error": repr(error),
            }


async def main(browser) -> None:
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    state_order = list(HISTORY_STATES)
    random.shuffle(state_order)

    successful = 0
    failures = []

    for sample_index in range(NUM_SAMPLES):
        base_data = generate_history_data(
            sample_index=sample_index,
            avatars_dir=AVATARS_DIR,
        )

        page_data = apply_history_state(
            base_data,
            state_order[sample_index % len(state_order)],
        )

        mode = (
            random.choice(["light", "dark"])
            if THEME_MODE == "random"
            else THEME_MODE
        )

        theme = generate_accessible_theme(mode=mode)

        results = await asyncio.gather(*[
            render_history_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                page_data=page_data,
                theme=theme,
                system=generate_system_data(
                    style="random",
                    icon_density="random",
                    viewport=viewport,
                ),
                viewport=viewport,
            )
            for viewport in viewports
        ])

        successful += sum(r["status"] == "success" for r in results)
        failures.extend(r for r in results if r["status"] == "failed")

    print(
        f"[TINYPAL HISTORY COMPLETE] "
        f"successful={successful} failed={len(failures)}"
    )

    if failures:
        raise RuntimeError(
            f"{len(failures)} history jobs failed. "
            "See the errors above."
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