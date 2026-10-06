

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
from social_media.steam.generators.library_generator import (
    generate_library_data,
)
from social_media.steam.renderers.common_renderer import (
    render_steam_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 20

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
# Render One Parallel Library Job
# ==========================================================

async def render_one_library_job(
    browser,
    semaphore,
    sample_index: int,
    library_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                "\n"
                "========================================"
            )

            print("STEAM LIBRARY")
            print("Sample:", sample_index)
            print("Theme:", theme["mode"])
            print("Viewport:", viewport["name"])

            print(
                "========================================"
            )

            await render_steam_page(

                browser=browser,

                sample_index=sample_index,

                page_type="library",

                template_name="library.html",

                context_key="library",

                page_data=library_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="library",

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "theme": theme["mode"],
                "viewport": viewport["name"],
            }

        except Exception as error:

            return {
                "status": "failed",
                "sample_index": sample_index,
                "theme": theme["mode"],
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main Generation
# ==========================================================

async def main(
    browser,
):

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    print(
        "Steam Library Dataset Generation | "
        f"jobs={NUM_SAMPLES * len(viewports)} | "
        f"workers={MAX_CONCURRENT_WORKERS}"
    )

    for sample_index in range(
        1,
        NUM_SAMPLES + 1,
    ):

        library_data = generate_library_data()

        system = generate_system_data()

        theme = generate_theme()

        for viewport in viewports:

            jobs.append(

                render_one_library_job(

                    browser=browser,

                    semaphore=semaphore,

                    sample_index=sample_index,

                    library_data=library_data,

                    system=system,

                    theme=theme,

                    viewport=viewport,
                )
            )

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
            "| Theme:", result["theme"],
            "| Viewport:", result["viewport"],
            "| Error:", result["error"],
        )


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:

            await main(
                browser
            )

        finally:

            await browser.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )