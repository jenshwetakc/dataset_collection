from __future__ import annotations

import asyncio
import random

from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.common.dynamic_system_generator import (
    generate_system_data,
)
from social_media.pinterest.generators.board_generator import (
    BOARD_STATES,
    create_board_state,
    generate_board_data,
)
from social_media.pinterest.renderers.common_renderer import (
    render_page,
)


PINTEREST_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = PINTEREST_ROOT / "templates"
OUTPUT_ROOT = PINTEREST_ROOT / "output"


# ==========================================================
# Configuration
# ==========================================================

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

STATES = BOARD_STATES

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MAX_CONCURRENT_WORKERS = 4

SAVE_VISUALIZATIONS = True

SYSTEM_STYLE = "random"
ICON_DENSITY = "random"


def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(mode=mode)


async def render_one_board_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    pinterest: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = pinterest["state"]

        metadata = {
            "sample_index": sample_index,
            "state": state,
            "viewport": viewport["name"],
            "theme": theme["mode"],
        }

        try:
            print(
                "[PINTEREST BOARD]",
                metadata,
                "system=",
                system["style"],
            )

            # For annotation purposes, the signed-out
            # banner follows your popup exclusion rule too.
            render_system = system

            if state == "signed_out_banner":
                # base.html checks popup_visible to exclude
                # system chrome. Set it only in the render
                # context; board.html still identifies the
                # banner using the state.
                pinterest = {
                    **pinterest,
                    "popup_visible": True,
                }

            await render_page(
                browser=browser,
                sample_index=sample_index,

                page_type=f"pinterest_board_{state}",
                template_name="board.html",
                context_key="pinterest",

                page_data=pinterest,
                system=render_system,
                theme=theme,
                viewport=viewport,

                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,

                output_subdir="board",

                annotation_profiles=ANNOTATION_PROFILES,

                min_visible_ratio=0.20,

                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=(
                    [0]
                    if state != "board"
                    else SCROLL_PERCENTAGES
                ),

                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                "status": "success",
                **metadata,
            }

        except Exception as error:
            print(
                "[PINTEREST BOARD FAILED]",
                metadata,
                "error=",
                repr(error),
            )

            return {
                "status": "failed",
                **metadata,
                "error": str(error),
            }


async def main(browser) -> None:
    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "MAX_CONCURRENT_WORKERS must be at least 1."
        )

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError(
            "Enable at least one capture mode."
        )

    viewports = get_viewports_by_names(VIEWPORTS)

    if not viewports:
        raise ValueError("No viewports were selected.")

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    total_successful = 0
    total_failed = 0

    for sample_index in range(NUM_SAMPLES):
        base_data = generate_board_data()

        state_data = {
            state: create_board_state(base_data, state)
            for state in STATES
        }

        theme = generate_theme()

        systems = {
            viewport["name"]: generate_system_data(
                style=SYSTEM_STYLE,
                icon_density=ICON_DENSITY,
                viewport=viewport,
            )
            for viewport in viewports
        }

        jobs = [
            render_one_board_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                pinterest=state_data[state],
                system=systems[viewport["name"]],
                theme=theme,
                viewport=viewport,
            )
            for viewport in viewports
            for state in STATES
        ]

        results = await asyncio.gather(*jobs)

        successful = sum(
            result["status"] == "success"
            for result in results
        )

        failed = len(results) - successful

        total_successful += successful
        total_failed += failed

        print(
            "[PINTEREST BOARD SAMPLE COMPLETE]",
            f"sample={sample_index}",
            f"successful={successful}",
            f"failed={failed}",
        )

    print(
        "\n[PINTEREST BOARD COMPLETE]",
        f"successful={total_successful}",
        f"failed={total_failed}",
    )

    if total_failed:
        raise RuntimeError(
            f"{total_failed} board renders failed."
        )


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