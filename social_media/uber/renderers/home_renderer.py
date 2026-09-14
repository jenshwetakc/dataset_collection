from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.common_renderer import resolve_viewports
from social_media.common.palette_generator import (
    generate_accessible_theme,
)



from social_media.uber.generators.home_generator import (
    generate_home_data,
)

from social_media.uber.renderers.common_renderer import (
    render_uber_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 5


VIEWPORT_MODE = "selected"

#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "desktop_fhd",
# ]
#
#
# # ANNOTATION_PROFILES = [
# #     "big_components",
# #     "components",
# #     "small_elements",
# #     "icons_only",
# # ]
# ANNOTATION_PROFILES = [
#     "big_components",
#     "small_elements",
# ]
#
#
# THEME_MODE = "random"
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
# System Data
# ==========================================================
#
# If you already have generate_system_data() in your common
# generator, replace this function with that import.
#
# This local fallback keeps the Uber renderer runnable.
# ==========================================================

def generate_system_data() -> dict:

    hour = random.randint(
        0,
        23,
    )

    minute = random.randint(
        0,
        59,
    )


    notification_icons = random.sample(
        [
            "mail",
            "chat",
            "notifications",
            "calendar_month",
            "music_note",
        ],
        k=random.randint(
            0,
            2,
        ),
    )


    return {

        "status_bar_variant":
            random.choice(
                [
                    "standard",
                    "compact",
                ]
            ),

        "time_text":
            f"{hour:02d}:{minute:02d}",

        "notifications": {
            "icons":
                notification_icons,
        },

        "system_states":
            random.sample(
                [
                    "alarm",
                    "bluetooth",
                    "do_not_disturb_on",
                ],
                k=random.randint(
                    0,
                    1,
                ),
            ),

        "cellular": {

            "available":
                True,

            "level":
                random.randint(
                    2,
                    4,
                ),

            "type":
                random.choice(
                    [
                        "5G",
                        "LTE",
                        "4G",
                    ]
                ),
        },

        "wifi": {

            "connected":
                random.choice(
                    [
                        True,
                        True,
                        False,
                    ]
                ),

            "level":
                random.randint(
                    1,
                    3,
                ),
        },

        "battery": {

            "level":
                random.randint(
                    18,
                    100,
                ),

            "charging":
                random.choice(
                    [
                        False,
                        False,
                        True,
                    ]
                ),

            "battery_saver":
                random.choice(
                    [
                        False,
                        False,
                        False,
                        True,
                    ]
                ),
        },
    }


# ==========================================================
# Theme Resolver
# ==========================================================

def generate_theme() -> dict:

    if THEME_MODE == "light":

        return generate_accessible_theme(
            mode="light"
        )


    if THEME_MODE == "dark":

        return generate_accessible_theme(
            mode="dark"
        )


    return generate_accessible_theme(
        mode=random.choice(
            [
                "light",
                "dark",
            ]
        )
    )


# ==========================================================
# Render
# ==========================================================

async def main():

    viewports = resolve_viewports(

        mode=
            VIEWPORT_MODE,

        selected=
            SELECTED_VIEWPORTS,
    )


    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )


        try:

            for sample_index in range(
                1,
                NUM_SAMPLES + 1,
            ):

                # ------------------------------------------
                # Generate once per sample
                # ------------------------------------------

                home_data = (
                    generate_home_data()
                )

                system_data = (
                    generate_system_data()
                )

                theme = (
                    generate_theme()
                )


                # ------------------------------------------
                # Render all selected viewports
                # ------------------------------------------

                for viewport in viewports:

                    print(
                        "\n"
                        "======================================"
                    )

                    print(
                        "Rendering Uber Home"
                    )

                    print(
                        "Sample:",
                        sample_index,
                    )

                    print(
                        "Viewport:",
                        viewport["name"],
                    )

                    print(
                        "Theme:",
                        theme["mode"],
                    )

                    print(
                        "======================================"
                    )


                    await render_uber_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "home",

                        template_name=
                            "home.html",

                        context_key=
                            "home",

                        page_data=
                            home_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        annotation_profiles=
                            ANNOTATION_PROFILES,


                        # ==================================
                        # Full + Viewport Capture
                        # ==================================

                        capture_full_page=
                            True,

                        capture_viewports=
                            True,


                        # Home is mainly map-based.
                        #
                        # Desktop panel can scroll, but on
                        # mobile the document itself should
                        # normally remain fixed.
                        #
                        # Common renderer will automatically
                        # eliminate duplicate positions.
                        scroll_percentages=[
                            0,
                            10,
                            20,
                            30,
                            40,
                            50,
                            60,
                            70,
                            80,
                            90,
                            100,
                        ],
                    )


        finally:

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )