from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.system_generator import (
    generate_system_data,
)
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.pycharm.generators.partial_overlay_generator import (
    OVERLAY_STATES,
    generate_partial_overlay_data,
)
from social_media.pycharm.renderers.common_renderer import (
    render_pycharm_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 20

SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_android",
    "standard_iphone",
    "large_mobile",
    "mobile_landscape",
    "tablet_portrait",
    "large_tablet_portrait",
    "tablet_landscape",
    "foldable",
    "small_laptop",
    "laptop",
    "large_laptop",
    "desktop_fhd",
    "desktop_qhd",
    "desktop_4k",
    "ultrawide",
]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
]

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:

    mode = (
        random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render One Parallel Partial-Overlay Job
# ==========================================================

async def render_one_partial_overlay_job(
    browser,
    semaphore,
    sample_index: int,
    state: str,
    overlay_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                "[PYCHARM PARTIAL OVERLAY]",
                "sample=",
                sample_index,
                "state=",
                state,
                "viewport=",
                viewport["name"],
                "theme=",
                theme["mode"],
            )

            await render_pycharm_page(

                browser=browser,

                sample_index=sample_index,

                page_type="partial_overlay",

                template_name="partial_overlay.html",

                context_key="overlay",

                page_data=overlay_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="partial_overlay",

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": state,
                "theme": theme["mode"],
                "viewport": viewport["name"],
            }

        except Exception as error:

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": state,
                "theme": theme["mode"],
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main Generation
# ==========================================================

async def main(
    browser,
) -> None:

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    print(
        "PyCharm Partial Overlay Dataset Generation | "
        f"jobs={len(OVERLAY_STATES) * NUM_SAMPLES_PER_STATE * len(viewports)} | "
        f"workers={MAX_CONCURRENT_WORKERS}"
    )

    sample_index = 0

    for state in OVERLAY_STATES:

        for _ in range(
            NUM_SAMPLES_PER_STATE,
        ):

            overlay_data = (
                generate_partial_overlay_data(
                    state=state
                )
            )

            system = generate_system_data()

            theme = generate_theme()

            for viewport in viewports:

                jobs.append(

                    render_one_partial_overlay_job(

                        browser=browser,

                        semaphore=semaphore,

                        sample_index=sample_index,

                        state=state,

                        overlay_data=overlay_data,

                        system=system,

                        theme=theme,

                        viewport=viewport,
                    )
                )

            sample_index += 1

    results = await asyncio.gather(
        *jobs
    )

    successful_results = [
        result
        for result in results
        if result["status"] == "success"
    ]

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    print(
        "Generation complete | "
        f"successful={len(successful_results)} | "
        f"failed={len(failed_results)}"
    )

    for result in failed_results:

        print(
            "[FAILED]",
            "Sample:", result["sample_index"],
            "| State:", result["state"],
            "| Theme:", result["theme"],
            "| Viewport:", result["viewport"],
            "| Error:", result["error"],
        )


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run() -> None:

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        try:

            await main(
                browser
            )

        finally:

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )