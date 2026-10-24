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
from social_media.pinterest.generators.profile_generator import (
    PROFILE_STATES,
    create_profile_state,
    generate_profile_data,
)
from social_media.pinterest.renderers.common_renderer import (
    render_page,
)


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

STATES = PROFILE_STATES

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


async def render_one_profile_job(
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
                "[PINTEREST PROFILE]",
                metadata,
                "system=",
                system["style"],
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,

                page_type=f"pinterest_profile_{state}",
                template_name="profile.html",
                context_key="pinterest",

                page_data=pinterest,
                system=system,
                theme=theme,
                viewport=viewport,

                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,

                # Every state shares this output location.
                output_subdir="profile",

                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=0.20,

                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=(
                    [0]
                    if pinterest["popup_visible"]
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
                "[PINTEREST PROFILE FAILED]",
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

    if not STATES:
        raise ValueError("Select at least one state.")

    viewports = get_viewports_by_names(VIEWPORTS)

    if not viewports:
        raise ValueError("No viewports were selected.")

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    total_successful = 0
    total_failed = 0

    for sample_index in range(NUM_SAMPLES):
        # Generate person and images once per sample.
        base_data = generate_profile_data()

        data_by_state = {
            state: create_profile_state(base_data, state)
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
            render_one_profile_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                pinterest=data_by_state[state],
                system=systems[viewport["name"]],
                theme=theme,
                viewport=viewport,
            )
            for viewport in viewports
            for state in STATES
        ]

        # Batch by sample to limit pending image-heavy jobs.
        results = await asyncio.gather(*jobs)

        successful = sum(
            result["status"] == "success"
            for result in results
        )

        failed = len(results) - successful

        total_successful += successful
        total_failed += failed

        print(
            "[PINTEREST PROFILE SAMPLE COMPLETE]",
            f"sample={sample_index}",
            f"successful={successful}",
            f"failed={failed}",
        )

    print(
        "\n[PINTEREST PROFILE COMPLETE]",
        f"successful={total_successful}",
        f"failed={total_failed}",
    )

    if total_failed:
        raise RuntimeError(
            f"{total_failed} profile renders failed. "
            "See the error messages above."
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