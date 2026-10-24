from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

from social_media.uptodate.generators.account_generator import (
    ACCOUNT_STATES,
    apply_account_state,
    generate_account_data,
)
from social_media.uptodate.renderers.common_renderer import render_page


UPTODATE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = UPTODATE_ROOT / "templates"
OUTPUT_ROOT = UPTODATE_ROOT / "output"

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


async def render_account_job(
    *,
    browser,
    semaphore,
    sample_index,
    page_data,
    theme,
    viewport,
) -> dict:
    async with semaphore:
        state = page_data["state"]

        try:
            print(
                f"[UPTODATE ACCOUNT] sample={sample_index} "
                f"state={state} viewport={viewport['name']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"account_{state}",
                template_name="account.html",
                context_key="uptodate",
                page_data=page_data,
                system=generate_system_data(
                    style="random",
                    icon_density="random",
                    viewport=viewport,
                ),
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="account",
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
            return {"status": "success"}

        except Exception as error:
            print(
                f"[UPTODATE ACCOUNT FAILED] sample={sample_index} "
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

    states = list(ACCOUNT_STATES)
    random.shuffle(states)

    successful = 0
    failures = []

    for sample_index in range(NUM_SAMPLES):
        page_data = apply_account_state(
            generate_account_data(sample_index),
            states[sample_index % len(states)],
        )

        mode = (
            random.choice(["light", "dark"])
            if THEME_MODE == "random" else THEME_MODE
        )
        theme = generate_accessible_theme(mode=mode)

        if page_data["active_section"] == "appearance":
            page_data["appearance_choice"] = mode

        results = await asyncio.gather(*[
            render_account_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                page_data=page_data,
                theme=theme,
                viewport=viewport,
            )
            for viewport in viewports
        ])

        successful += sum(
            result["status"] == "success" for result in results
        )
        failures.extend(
            result for result in results
            if result["status"] == "failed"
        )

    print(
        f"[UPTODATE ACCOUNT COMPLETE] "
        f"successful={successful} failed={len(failures)}"
    )

    if failures:
        raise RuntimeError(
            f"{len(failures)} account jobs failed. See errors above."
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