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

from social_media.webtoon.generators.home_generator import (
    STATES,
    generate_home_page,
    make_state,
)

from social_media.webtoon.renderers.common_renderer import (
    render_page,
)


# ==========================================================
# Paths
# ==========================================================

WEBTOON_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = WEBTOON_ROOT / "templates"

OUTPUT_ROOT = WEBTOON_ROOT / "output"


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

WEBTOON_STATES = list(STATES)

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

SAVE_VISUALIZATIONS = True


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

async def render_one_home_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    webtoon: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[WEBTOON HOME]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"theme={theme['mode']}",
                f"system={system['style']}",
            )

            # Popup states capture only the initial position.
            scroll_percentages = (
                [0]
                if webtoon["popup"]
                else SCROLL_PERCENTAGES
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"webtoon_home_{state}",
                template_name="home.html",
                context_key="webtoon",
                page_data=webtoon,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="home",
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=0.20,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=scroll_percentages,
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
                "[WEBTOON HOME FAILED]",
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

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
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

    unknown_states = (
        set(WEBTOON_STATES)
        - set(STATES)
    )

    if unknown_states:
        raise ValueError(
            f"Unknown WEBTOON states: "
            f"{sorted(unknown_states)}"
        )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS,
    )

    successful = 0
    failed = 0

    print(
        "\n[WEBTOON CONFIGURATION]",
        f"samples={NUM_SAMPLES}",
        f"states={len(WEBTOON_STATES)}",
        f"viewports={len(viewports)}",
        f"workers={MAX_CONCURRENT_WORKERS}",
    )

    for sample_index in range(NUM_SAMPLES):
        # Generate content and theme once per sample.
        # Reuse them across states and viewports.
        content = generate_home_page(
            package_root="social_media",
        )

        theme = generate_theme()

        state_data = {
            state: make_state(
                content,
                state,
            )
            for state in WEBTOON_STATES
        }

        jobs = []

        for viewport in viewports:
            # Generate platform chrome per viewport.
            # Reuse it across this viewport's page states.
            system = generate_system_data(
                style=SYSTEM_STYLE,
                icon_density=ICON_DENSITY,
                viewport=viewport,
            )

            for state in WEBTOON_STATES:
                jobs.append(
                    render_one_home_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        state=state,
                        webtoon=state_data[state],
                        system=system,
                        theme=theme,
                        viewport=viewport,
                    )
                )

        # Process one sample at a time to avoid retaining
        # every sample's embedded image data in memory.
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
        "\n[WEBTOON HOME COMPLETE]",
        f"successful={successful}",
        f"failed={failed}",
    )

    if failed:
        raise RuntimeError(
            f"{failed} WEBTOON render jobs failed. "
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