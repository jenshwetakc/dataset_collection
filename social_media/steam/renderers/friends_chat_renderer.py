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

from social_media.steam.generators.friends_chat_generator import (
    generate_friends_chat_data,
)

from social_media.steam.renderers.common_renderer import (
    render_steam_page,
)


# ==========================================================
# Configuration
# ==========================================================
#
# NUM_SAMPLES = 3
#
#
# SELECTED_VIEWPORTS = [
#
#     "small_mobile",
#
#     "desktop_fhd",
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
# ]
#
#
# THEME_MODE = "random"
#
#
# CAPTURE_FULL_PAGE = True
#
# CAPTURE_VIEWPORTS = True
#
#
# SCROLL_PERCENTAGES = [
#
#     0,
#
#     10,
#
#     20,
#
#     30,
#
#     40,
#
#     50,
#
#     60,
#
#     70,
#
#     80,
#
#     90,
#
#     100,
# ]
NUM_SAMPLES = 18
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


THEME_MODE = "random"

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

# ==========================================================
# Theme
# ==========================================================

def generate_theme():

    if THEME_MODE == "random":

        mode = random.choice([
            "light",
            "dark",
        ])

    else:

        mode = THEME_MODE


    return generate_accessible_theme(
        mode=mode
    )


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
                headless=True
            )
        )


        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                print(
                    "\n"
                    "========================================"
                )

                print(
                    "STEAM FRIENDS & CHAT"
                )

                print(
                    "Sample:",
                    sample_index,
                )

                print(
                    "========================================"
                )


                chat_data = (
                    generate_friends_chat_data()
                )


                system = (
                    generate_system_data()
                )


                theme = (
                    generate_theme()
                )


                for viewport in viewports:

                    await render_steam_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "friends_chat",

                        template_name=
                            "friends_chat.html",

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
                            "friends_chat",

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            CAPTURE_FULL_PAGE,

                        capture_viewports=
                            CAPTURE_VIEWPORTS,

                        scroll_percentages=
                            SCROLL_PERCENTAGES,
                    )


        finally:

            await browser.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )