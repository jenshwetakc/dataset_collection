from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.media_generator import ASSETS_ROOT
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

from social_media.capcut.generators.spaces_generator import (
    SPACES_STATES,
    apply_spaces_state,
    generate_spaces_data,
)
from social_media.capcut.renderers.common_renderer import render_page


CAPCUT_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = CAPCUT_ROOT / "templates"
OUTPUT_ROOT = CAPCUT_ROOT / "output"
THUMBNAILS_DIR = ASSETS_ROOT / "capcut"
AVATARS_DIR = ASSETS_ROOT / "capcut"

NUM_SAMPLES = 6

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


async def render_spaces_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    page_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = page_data["state"]

        try:
            print(
                f"[CAPCUT SPACES] sample={sample_index} "
                f"state={state} viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"spaces_{state}",
                template_name="spaces.html",
                context_key="capcut",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="spaces",
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=0.20,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0] if page_data["popup_visible"] else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[CAPCUT SPACES FAILED] sample={sample_index} "
                f"state={state} viewport={viewport['name']} "
                f"error={error!r}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
                "error": repr(error),
            }


async def main(browser) -> None:
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    states = list(SPACES_STATES)
    random.shuffle(states)

    successful = 0
    failures = []

    for sample_index in range(NUM_SAMPLES):
        base_data = generate_spaces_data(
            sample_index=sample_index,
            thumbnails_dir=THUMBNAILS_DIR,
            avatars_dir=AVATARS_DIR,
        )

        page_data = apply_spaces_state(
            base_data,
            states[sample_index % len(states)],
        )
        theme = generate_theme()

        results = await asyncio.gather(
            *[
                render_spaces_job(
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
        )

        successful += sum(
            result["status"] == "success" for result in results
        )
        failures.extend(
            result for result in results if result["status"] == "failed"
        )

    print(
        f"[CAPCUT SPACES COMPLETE] "
        f"successful={successful} failed={len(failures)}"
    )

    if failures:
        raise RuntimeError(
            f"{len(failures)} Spaces jobs failed. "
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