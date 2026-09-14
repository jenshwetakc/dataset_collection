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

from social_media.tinder.generators.chat_states_generator import (
    CHAT_STATES,
    generate_chat_states_data,
)

from social_media.tinder.renderers.common_renderer import (
    render_tinder_page,
)


# ==========================================================
# Configuration
# ==========================================================
#
# NUM_SAMPLES_PER_STATE = 2
#
#
# SELECTED_VIEWPORTS = [
#
#     "laptop",
#
#     "desktop_fhd",
#
# ]
#
#
# ANNOTATION_PROFILES = [
#
#     "big_components",
#
#     "components",
#
#     "small_elements",
#
#     "icons_only",
#
# ]
#
#
THEME_MODES = [

    "light",

    "dark",

]
NUM_SAMPLES_PER_STATE = 18
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
    "icons_only",
]


# THEME_MODES = "random"

# CAPTURE_FULL_PAGE = True
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


# ==========================================================
# Main
# ==========================================================

async def main():

    viewports = (
        get_viewports_by_names(
            SELECTED_VIEWPORTS
        )
    )


    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch(
                headless=True,
            )
        )


        try:

            global_sample_index = 0


            for state in CHAT_STATES:

                for state_sample_index in range(
                    NUM_SAMPLES_PER_STATE
                ):

                    chat_data = (
                        generate_chat_states_data(
                            state=state,
                        )
                    )


                    system = (
                        generate_system_data()
                    )


                    for theme_mode in THEME_MODES:

                        theme = (
                            generate_accessible_theme(

                                seed=random.choice(
                                    TINDER_SEEDS
                                ),

                                mode=
                                    theme_mode,
                            )
                        )


                        for viewport in viewports:

                            print(
                                "\n"
                                "===================================="
                            )

                            print(
                                "TINDER CHAT STATE"
                            )

                            print(
                                "state:",
                                state,
                            )

                            print(
                                "state sample:",
                                state_sample_index,
                            )

                            print(
                                "global sample:",
                                global_sample_index,
                            )

                            print(
                                "theme:",
                                theme_mode,
                            )

                            print(
                                "viewport:",
                                viewport["name"],
                            )

                            print(
                                "===================================="
                            )


                            await render_tinder_page(

                                browser=
                                    browser,

                                sample_index=
                                    global_sample_index,

                                page_type=
                                    f"chat_{state}",

                                template_name=
                                    "chat_states.html",

                                context_key=
                                    "chat",

                                page_data=
                                    chat_data,

                                system=
                                    system,

                                theme=
                                    theme,

                                viewport=
                                    viewport,

                                output_subdir=
                                    "chat_states",

                                annotation_profiles=
                                    ANNOTATION_PROFILES,

                                capture_full_page=
                                    True,

                                capture_viewports=
                                    True,

                                scroll_percentages=[
                                    0
                                ],
                            )


                    global_sample_index += 1


        finally:

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )