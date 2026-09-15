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

from social_media.booking.generators.booking_checkout_generator import (
    generate_booking_checkout_data,
)

from social_media.booking.renderers.common_renderer import (
    render_booking_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "desktop_fhd",
# ]
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


# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
# ]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]



THEME_MODE = "random"


# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
    20,
    40,
    60,
    80,
    100,
]


# ==========================================================
# Theme
# ==========================================================

def generate_sample_theme():

    if THEME_MODE == "random":

        mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

    else:

        mode = THEME_MODE


    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render
# ==========================================================

async def render():

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

                checkout_data = (
                    generate_booking_checkout_data()
                )

                system = (
                    generate_system_data()
                )

                theme = (
                    generate_sample_theme()
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    "BOOKING CHECKOUT:",
                    sample_index,
                )

                print(
                    "State:",
                    checkout_data[
                        "state"
                    ],
                )

                print(
                    "Theme:",
                    theme[
                        "mode"
                    ],
                )

                print(
                    "WCAG:",
                    theme[
                        "wcag_pass"
                    ],
                )

                print(
                    "======================================"
                )


                for viewport in viewports:

                    print(
                        "Rendering:",
                        viewport[
                            "name"
                        ],
                    )


                    await render_booking_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "booking_checkout",

                        template_name=
                            "booking_checkout.html",

                        context_key=
                            "checkout",

                        page_data=
                            checkout_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "booking_checkout",

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
# Main
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        render()
    )