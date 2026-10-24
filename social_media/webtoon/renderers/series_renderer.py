from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.common.dynamic_system_generator import (
    generate_system_data,
)

from social_media.webtoon.generators.series_generator import (
    SERIES_STATES,
    generate_series_data,
    apply_series_state,
)

from social_media.webtoon.renderers.common_renderer import (
    render_webtoon_page,
)


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

PAGE_STATES = list(SERIES_STATES)

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

SYSTEM_STYLE = "random"

ICON_DENSITY = "random"

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


# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:
    if THEME_MODE not in {
        "random",
        "light",
        "dark",
    }:
        raise ValueError(
            "THEME_MODE must be "
            "'random', 'light', or 'dark'."
        )

    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode,
    )


# ==========================================================
# Render Job
# ==========================================================

async def render_one_series_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    series: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    state = series["state"]

    async with semaphore:
        try:
            print(
                "[WEBTOON SERIES]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"theme={theme['mode']}",
            )

            scroll_positions = (
                [0]
                if series["popup"]
                else SCROLL_PERCENTAGES
            )

            await render_webtoon_page(
                browser=browser,
                sample_index=sample_index,

                # Prevent state files from overwriting
                # each other.
                page_type=f"series_{state}",

                template_name="series.html",

                # Existing base.html expects webtoon.
                context_key="webtoon",
                page_data=series,

                system=system,
                theme=theme,
                viewport=viewport,

                # Every series state shares this folder.
                output_subdir="series",

                annotation_profiles=(
                    ANNOTATION_PROFILES
                ),

                capture_full_page=(
                    CAPTURE_FULL_PAGE
                ),

                capture_viewports=(
                    CAPTURE_VIEWPORTS
                ),

                scroll_percentages=(
                    scroll_positions
                ),
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[WEBTOON SERIES FAILED]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"error={error!r}",
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": state,
                "viewport": viewport["name"],
                "error": repr(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "MAX_CONCURRENT_WORKERS must be at least 1."
        )

    if (
        not CAPTURE_FULL_PAGE
        and not CAPTURE_VIEWPORTS
    ):
        raise ValueError(
            "Enable at least one capture mode."
        )

    viewports = get_viewports_by_names(
        VIEWPORTS,
    )

    if not viewports:
        raise ValueError(
            "No viewports were resolved."
        )

    if not PAGE_STATES:
        raise ValueError(
            "Select at least one page state."
        )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS,
    )

    successful = 0
    failed = 0

    for sample_index in range(NUM_SAMPLES):
        # Reuse content across states and viewports.
        content = generate_series_data()

        # Reuse one theme across the sample.
        theme = generate_theme()

        state_data = [
            apply_series_state(
                content,
                state,
            )
            for state in PAGE_STATES
        ]

        jobs = []

        for viewport in viewports:
            # System style is resolved for this viewport.
            system = generate_system_data(
                style=SYSTEM_STYLE,
                icon_density=ICON_DENSITY,
                viewport=viewport,
            )

            for series in state_data:
                jobs.append(
                    render_one_series_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        series=series,
                        system=system,
                        theme=theme,
                        viewport=viewport,
                    )
                )

        # Process one sample at a time to limit memory
        # retained by embedded image data.
        results = await asyncio.gather(
            *jobs,
        )

        sample_successful = sum(
            result["status"] == "success"
            for result in results
        )

        sample_failed = (
            len(results)
            - sample_successful
        )

        successful += sample_successful
        failed += sample_failed

        print(
            "[WEBTOON SAMPLE COMPLETE]",
            f"sample={sample_index}",
            f"successful={sample_successful}",
            f"failed={sample_failed}",
        )

    print(
        "\n[WEBTOON SERIES COMPLETE]",
        f"successful={successful}",
        f"failed={failed}",
    )

    if failed:
        raise RuntimeError(
            f"{failed} WEBTOON series jobs failed. "
            "See the failure messages above."
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