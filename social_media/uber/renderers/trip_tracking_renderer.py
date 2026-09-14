from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.renderer import (
    resolve_viewports,
)

from social_media.uber.generators.trip_tracking_generator import (
    generate_trip_tracking_data,
)

from social_media.uber.renderers.common_renderer import (
    render_uber_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 2


VIEWPORT_MODE = "selected"

#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "tablet_portrait",
#     "laptop",
#     "desktop_fhd",
# ]
#
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
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
# System Generator
#
# Replace with your shared generate_system_data import
# if that already exists.
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

    return {

        "status_bar_variant":
            "standard",

        "time_text":
            f"{hour:02d}:{minute:02d}",

        "notifications": {
            "icons":
                random.sample(
                    [
                        "mail",
                        "chat",
                        "notifications",
                    ],
                    k=random.randint(
                        0,
                        2,
                    ),
                ),
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
                    20,
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
                False,
        },
    }


# ==========================================================
# Theme
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
# Main
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

                trip_data = (
                    generate_trip_tracking_data()
                )

                system_data = (
                    generate_system_data()
                )

                theme = (
                    generate_theme()
                )


                for viewport in viewports:

                    print(
                        "\n"
                        "======================================"
                    )

                    print(
                        "Rendering Uber Trip Tracking"
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
                            "trip_tracking",

                        template_name=
                            "trip_tracking.html",

                        context_key=
                            "trip_tracking",

                        page_data=
                            trip_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            True,

                        capture_viewports=
                            True,

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
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )