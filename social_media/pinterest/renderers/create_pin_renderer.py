from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.viewport import get_viewports_by_names
from social_media.pinterest.generators.create_pin_generator import (
    CREATE_PIN_STATES,
    create_pin_state,
    generate_create_pin_data,
)
from social_media.pinterest.renderers.common_renderer import render_page


PINTEREST_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PINTEREST_ROOT / "templates"
OUTPUT_ROOT = PINTEREST_ROOT / "output"

NUM_SAMPLES = 5

VIEWPORTS = [
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

STATES = CREATE_PIN_STATES
ANNOTATION_PROFILES = ["big_components", "small_elements"]

THEME_MODE = "random"
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]

MAX_CONCURRENT_WORKERS = 4
SAVE_VISUALIZATIONS = True


def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )
    return generate_accessible_theme(mode=mode)


async def render_one_job(
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
                "[PINTEREST CREATE PIN]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"theme={theme['mode']}",
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"pinterest_create_pin_{state}",
                template_name="create_pin.html",
                context_key="pinterest",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="create_pin",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0]
                    if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {"status": "success"}

        except Exception as error:
            print(
                "[PINTEREST CREATE PIN FAILED]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"error={error}",
            )

            return {
                "status": "failed",
                "error": str(error),
            }


async def main(browser) -> None:
    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError("MAX_CONCURRENT_WORKERS must be at least 1.")

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError("Enable at least one capture mode.")

    if not STATES:
        raise ValueError("Select at least one state.")

    unknown_states = set(STATES) - set(CREATE_PIN_STATES)

    if unknown_states:
        raise ValueError(f"Unknown states: {sorted(unknown_states)}")

    viewports = get_viewports_by_names(VIEWPORTS)

    if not viewports:
        raise ValueError("Select at least one viewport.")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    successful = 0
    failed = 0

    for sample_index in range(NUM_SAMPLES):
        base_data = generate_create_pin_data()
        theme = generate_theme()

        state_data = [
            create_pin_state(base_data, state)
            for state in STATES
        ]

        jobs = []

        for viewport in viewports:
            system = generate_system_data(viewport=viewport)

            for page_data in state_data:
                jobs.append(
                    render_one_job(
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

        successful += sum(
            result["status"] == "success"
            for result in results
        )
        failed += sum(
            result["status"] == "failed"
            for result in results
        )

    print(
        "\n[PINTEREST CREATE PIN COMPLETE]",
        f"successful={successful}",
        f"failed={failed}",
    )

    if failed:
        raise RuntimeError(f"{failed} Create Pin render jobs failed.")


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())