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
# from social_media.tinder.generators.discover_states_generator import (
#     DISCOVER_STATES,
#     generate_discover_states_data,
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
# # NUM_SAMPLES_PER_STATE = 2
# #
# #
# # SELECTED_VIEWPORTS = [
# #
# #     "foldable",
# #
# #     "laptop",
# #
# # ]
# #
# #
# # ANNOTATION_PROFILES = [
# #
# #     "big_components",
# #     "components",
# #     "small_elements",
# #     "icons_only",
# #
# # ]
# #
# #
# THEME_MODES = [
#
#     "light",
#     "dark",
#
# ]
# NUM_SAMPLES_PER_STATE = 18
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
# ANNOTATION_PROFILES = [
#     "big_components",
#     "small_elements",
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
# TINDER_SEEDS = [
#
#     "#FD5068",
#     "#FF4458",
#     "#FE3C72",
#     "#E94057",
#
# ]
#
#
# # ==========================================================
# # Main
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
#             global_sample_index = 0
#
#
#             for state in DISCOVER_STATES:
#
#                 for state_sample_index in range(
#                     NUM_SAMPLES_PER_STATE
#                 ):
#
#                     discover_data = (
#                         generate_discover_states_data(
#                             state=state,
#                         )
#                     )
#
#
#                     system = (
#                         generate_system_data()
#                     )
#
#
#                     for theme_mode in THEME_MODES:
#
#                         theme = (
#                             generate_accessible_theme(
#
#                                 seed=random.choice(
#                                     TINDER_SEEDS
#                                 ),
#
#                                 mode=
#                                     theme_mode,
#                             )
#                         )
#
#
#                         for viewport in viewports:
#
#                             print(
#                                 "\n"
#                                 "===================================="
#                             )
#
#                             print(
#                                 "TINDER DISCOVER STATE"
#                             )
#
#                             print(
#                                 "state:",
#                                 state,
#                             )
#
#                             print(
#                                 "sample:",
#                                 state_sample_index,
#                             )
#
#                             print(
#                                 "theme:",
#                                 theme_mode,
#                             )
#
#                             print(
#                                 "viewport:",
#                                 viewport["name"],
#                             )
#
#                             print(
#                                 "===================================="
#                             )
#
#
#                             await render_tinder_page(
#
#                                 browser=
#                                     browser,
#
#                                 sample_index=
#                                     global_sample_index,
#
#                                 page_type=
#                                     f"discover_{state}",
#
#                                 template_name=
#                                     "discover_states.html",
#
#                                 context_key=
#                                     "discover",
#
#                                 page_data=
#                                     discover_data,
#
#                                 system=
#                                     system,
#
#                                 theme=
#                                     theme,
#
#                                 viewport=
#                                     viewport,
#
#                                 output_subdir=
#                                     "discover_states",
#
#                                 annotation_profiles=
#                                     ANNOTATION_PROFILES,
#
#                                 capture_full_page=
#                                     True,
#
#                                 capture_viewports=
#                                     True,
#
#                                 scroll_percentages=[
#                                     0
#                                 ],
#                             )
#
#
#                     global_sample_index += 1
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

from social_media.tinder.generators.discover_states_generator import (
    DISCOVER_STATES,
    generate_discover_states_data,
)

from social_media.tinder.renderers.common_renderer import (
    render_tinder_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 30

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
# Render One Parallel Discover-State Job
# ==========================================================

async def render_one_discover_state_job(
    browser,
    semaphore,
    state: str,
    state_sample_index: int,
    global_sample_index: int,
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

            print("TINDER DISCOVER STATE")
            print("State:", state)
            print("State sample:", state_sample_index)
            print("Global sample:", global_sample_index)
            print("Theme:", theme_mode)
            print("Viewport:", viewport["name"])

            print(
                "===================================="
            )

            await render_tinder_page(

                # Shared browser; the common renderer creates
                # and closes an independent page per task.
                browser=browser,

                sample_index=global_sample_index,

                page_type=f"discover_{state}",

                template_name="discover_states.html",

                context_key="discover",

                page_data=discover_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="discover_states",

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {

                "status": "success",

                "state": state,

                "state_sample_index": state_sample_index,

                "global_sample_index": global_sample_index,

                "theme": theme_mode,

                "viewport": viewport["name"],
            }

        except Exception as error:

            return {

                "status": "failed",

                "state": state,

                "state_sample_index": state_sample_index,

                "global_sample_index": global_sample_index,

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

    total_jobs = (

        len(DISCOVER_STATES)

        * NUM_SAMPLES_PER_STATE

        * len(THEME_MODES)

        * len(viewports)
    )

    print(
        "\n"
        "===================================="
    )

    print("Tinder Discover States Dataset Generation")
    print("States:", len(DISCOVER_STATES))

    print(
        "Samples per state:",
        NUM_SAMPLES_PER_STATE,
    )

    print("Themes:", len(THEME_MODES))
    print("Viewports:", len(viewports))
    print("Total jobs:", total_jobs)

    print(
        "Parallel workers:",
        MAX_CONCURRENT_WORKERS,
    )

    print(
        "===================================="
    )


    global_sample_index = 0


    # One Discover-state UI variation per state/sample.
    # It is rendered in both theme modes and every viewport.
    for state in DISCOVER_STATES:

        for state_sample_index in range(
            NUM_SAMPLES_PER_STATE,
        ):

            discover_data = (
                generate_discover_states_data(
                    state=state,
                )
            )

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

                        render_one_discover_state_job(

                            browser=browser,

                            semaphore=semaphore,

                            state=state,

                            state_sample_index=state_sample_index,

                            global_sample_index=global_sample_index,

                            discover_data=discover_data,

                            system=system,

                            theme=theme,

                            theme_mode=theme_mode,

                            viewport=viewport,
                        )
                    )

            global_sample_index += 1


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

            "State:",
            result["state"],

            "| Global sample:",
            result["global_sample_index"],

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