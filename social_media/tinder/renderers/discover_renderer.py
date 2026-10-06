# from __future__ import annotations
#
# import asyncio
# import random
#
# from playwright.async_api import (
#     async_playwright,
# )
#
# from social_media.common.palette_generator import (
#     generate_accessible_theme,
# )
#
# from social_media.common.system_generator import (
#     generate_system_data,
# )
#
# from social_media.common.viewport import (
#     get_viewports_by_names,
# )
#
# from social_media.tinder.generators.discover_generator import (
#     generate_discover_data,
# )
#
# from social_media.tinder.renderers.common_renderer import (
#     render_tinder_page,
# )
#
#
# # ==========================================================
# # Configuration
# # ==========================================================
#
# # NUM_SAMPLES = 3
# #
# #
# # SELECTED_VIEWPORTS = [
# #
# #
# #     "foldable",
# #
# #     "small_laptop",
# # ]
# #
# #
# # ANNOTATION_PROFILES = [
# #
# #     "big_components",
# #
# #     "components",
# #
# #     "small_elements",
# #
# #     "icons_only",
# #
# # ]
# #
# #
# THEME_MODES = [
#     "light",
#     "dark",
# ]
#
# #
# # CAPTURE_FULL_PAGE = True
# #
# # CAPTURE_VIEWPORTS = True
# #
# #
# # SCROLL_PERCENTAGES = [
# #
# #     0,
# #     10,
# #     20,
# #     30,
# #     40,
# #     50,
# #     60,
# #     70,
# #     80,
# #     90,
# #     100,
# #
# # ]
# NUM_SAMPLES = 18
# SELECTED_VIEWPORTS = [
#     "small_mobile",
#     "standard_android",
#     "standard_iphone",
#     "large_mobile",
#     "mobile_landscape",
#     "tablet_portrait",
#     "large_tablet_portrait",
#     "tablet_landscape",
#     "foldable",
#     "small_laptop",
#     "laptop",
#     "large_laptop",
#     "desktop_fhd",
#     "desktop_qhd",
#     "desktop_4k",
#     "ultrawide",
# ]
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "icons_only",
# ]
#
#
# # THEME_MODES = "random"
#
# # CAPTURE_FULL_PAGE = True
# CAPTURE_FULL_PAGE = False
#
# CAPTURE_VIEWPORTS = True
#
# SCROLL_PERCENTAGES = [
#     0,
#     25,
#     50,
#     75,
#     100,
# ]
#
# # ==========================================================
# # Tinder Seeds
# # ==========================================================
#
# TINDER_SEEDS = [
#
#     "#FD5068",
#
#     "#FF4458",
#
#     "#FE3C72",
#
#     "#E94057",
#
# ]
#
#
# # ==========================================================
# # Render
# # ==========================================================
#
# async def main():
#
#     viewports = (
#         get_viewports_by_names(
#             SELECTED_VIEWPORTS
#         )
#     )
#
#
#     async with async_playwright() as playwright:
#
#         browser = (
#             await playwright.chromium.launch(
#                 headless=True,
#             )
#         )
#
#
#         try:
#
#             for sample_index in range(
#                 NUM_SAMPLES
#             ):
#
#                 discover_data = (
#                     generate_discover_data()
#                 )
#
#
#                 system = (
#                     generate_system_data()
#                 )
#
#
#                 for theme_mode in THEME_MODES:
#
#                     theme = (
#                         generate_accessible_theme(
#
#                             seed=random.choice(
#                                 TINDER_SEEDS
#                             ),
#
#                             mode=theme_mode,
#                         )
#                     )
#
#
#                     for viewport in viewports:
#
#                         print(
#                             "\n"
#                             "===================================="
#                         )
#
#                         print(
#                             "TINDER DISCOVER"
#                         )
#
#                         print(
#                             "sample:",
#                             sample_index,
#                         )
#
#                         print(
#                             "theme:",
#                             theme_mode,
#                         )
#
#                         print(
#                             "viewport:",
#                             viewport["name"],
#                         )
#
#                         print(
#                             "===================================="
#                         )
#
#
#                         await render_tinder_page(
#
#                             browser=
#                                 browser,
#
#                             sample_index=
#                                 sample_index,
#
#                             page_type=
#                                 "discover",
#
#                             template_name=
#                                 "discover.html",
#
#                             context_key=
#                                 "discover",
#
#                             page_data=
#                                 discover_data,
#
#                             system=
#                                 system,
#
#                             theme=
#                                 theme,
#
#                             viewport=
#                                 viewport,
#
#                             output_subdir=
#                                 "discover",
#
#                             annotation_profiles=
#                                 ANNOTATION_PROFILES,
#
#                             capture_full_page=
#                                 CAPTURE_FULL_PAGE,
#
#                             capture_viewports=
#                                 CAPTURE_VIEWPORTS,
#
#                             scroll_percentages=
#                                 SCROLL_PERCENTAGES,
#                         )
#
#
#         finally:
#
#             await browser.close()
#
#
# # ==========================================================
# # Entry Point
# # ==========================================================
#
# if __name__ == "__main__":
#
#     asyncio.run(
#         main()
#     )

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

from social_media.tinder.generators.discover_generator import (
    generate_discover_data,
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

CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

TINDER_SEEDS = [
    "#FD5068",
    "#FF4458",
    "#FE3C72",
    "#E94057",
]

# Begin with 4 concurrent rendering jobs.
MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Render One Parallel Discover Job
# ==========================================================

async def render_one_discover_job(
    browser,
    semaphore,
    sample_index: int,
    discover_data: dict,
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

            print("TINDER DISCOVER")
            print("Sample:", sample_index)
            print("Theme:", theme_mode)
            print("Viewport:", viewport["name"])

            print(
                "===================================="
            )

            await render_tinder_page(

                # The shared Browser creates one independent
                # page for each parallel rendering task.
                browser=browser,

                sample_index=sample_index,

                page_type="discover",

                template_name="discover.html",

                context_key="discover",

                page_data=discover_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="discover",

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

    print("Tinder Discover Dataset Generation")
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


    # One Discover UI variation per sample.
    # Each sample is rendered across every theme and viewport.
    for sample_index in range(
        1,
        NUM_SAMPLES + 1,
    ):

        discover_data = generate_discover_data()

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

                    render_one_discover_job(

                        browser=browser,

                        semaphore=semaphore,

                        sample_index=sample_index,

                        discover_data=discover_data,

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