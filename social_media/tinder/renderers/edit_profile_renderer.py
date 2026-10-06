from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.tinder.generators.edit_profile_generator import (
    generate_edit_profile_data,
)

from social_media.tinder.renderers.common_renderer import (
    render_tinder_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 30

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

THEME_MODES = [
    "light",
    "dark",
]

TINDER_SEEDS = [
    "#FD5068",
    "#FF4458",
    "#FE3C72",
    "#E94057",
]

CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

# Begin with 4 concurrent browser rendering jobs.
MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Render One Parallel Edit-Profile Job
# ==========================================================

async def render_one_edit_profile_job(
    browser,
    semaphore,
    sample_index: int,
    edit_data: dict,
    system: dict,
    theme: dict,
    theme_mode: str,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                "\n"
                "===================================="
            )

            print("TINDER EDIT PROFILE")
            print("Sample:", sample_index)
            print("Theme:", theme_mode)
            print("Viewport:", viewport["name"])

            print(
                "===================================="
            )

            await render_tinder_page(

                # The common renderer opens and closes
                # an independent page for every job.
                browser=browser,

                sample_index=sample_index,

                page_type="edit_profile",

                template_name="edit_profile.html",

                context_key="edit",

                page_data=edit_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="edit_profile",

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {

                "status": "success",

                "sample_index": sample_index,

                "theme": theme_mode,

                "viewport": viewport["name"],
            }

        except Exception as error:

            return {

                "status": "failed",

                "sample_index": sample_index,

                "theme": theme_mode,

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
        "\n"
        "===================================="
    )

    print("Tinder Edit Profile Dataset Generation")
    print("Samples:", NUM_SAMPLES)
    print("Themes:", len(THEME_MODES))
    print("Viewports:", len(viewports))

    print(
        "Total jobs:",
        NUM_SAMPLES
        * len(THEME_MODES)
        * len(viewports),
    )

    print(
        "Parallel workers:",
        MAX_CONCURRENT_WORKERS,
    )

    print(
        "===================================="
    )


    # One edit-profile UI variation per sample.
    # The same variation is rendered in both themes
    # and across every selected viewport.
    for sample_index in range(
        1,
        NUM_SAMPLES + 1,
    ):

        edit_data = generate_edit_profile_data()

        system = generate_system_data()

        for theme_mode in THEME_MODES:

            theme = generate_accessible_theme(

                seed=random.choice(
                    TINDER_SEEDS
                ),

                mode=theme_mode,
            )

            for viewport in viewports:

                jobs.append(

                    render_one_edit_profile_job(

                        browser=browser,

                        semaphore=semaphore,

                        sample_index=sample_index,

                        edit_data=edit_data,

                        system=system,

                        theme=theme,

                        theme_mode=theme_mode,

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
        "\n"
        "===================================="
    )

    print("Generation complete")

    print(
        "Successful jobs:",
        len(successful_results),
    )

    print(
        "Failed jobs:",
        len(failed_results),
    )

    print(
        "===================================="
    )


    for result in failed_results:

        print(

            "[FAILED]",

            "Sample:",
            result["sample_index"],

            "| Theme:",
            result["theme"],

            "| Viewport:",
            result["viewport"],

            "| Error:",
            result["error"],
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
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )