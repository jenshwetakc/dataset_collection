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

from social_media.zillow.generators.rental_application_generator import (
    generate_rental_application_data,
)

from social_media.zillow.renderers.common_renderer import (
    render_zillow_page,
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
#     "standard_iphone",
#
#     "large_mobile",
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
# ]
#
#
# # ==========================================================
# # Theme
# # ==========================================================
#
# THEME_MODE = "random"
#
#
# # ==========================================================
# # Capture
# # ==========================================================
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
"small_elements"
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
# Theme Generator
# ==========================================================

def generate_theme():

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

                rental_data = (
                    generate_rental_application_data()
                )


                system_data = (
                    generate_system_data()
                )


                theme = (
                    generate_theme()
                )


                print(
                    "\n"
                    "=========================================="
                )

                print(
                    "ZILLOW RENTAL APPLICATION"
                )

                print(
                    "=========================================="
                )

                print(
                    "Sample:",
                    sample_index,
                )

                print(
                    "Property:",
                    rental_data[
                        "property"
                    ][
                        "address"
                    ],
                )

                print(
                    "Progress:",
                    rental_data[
                        "application"
                    ][
                        "progress_percent"
                    ],
                )

                print(
                    "Theme:",
                    theme[
                        "mode"
                    ],
                )


                for viewport in viewports:

                    print(
                        "\nRendering:",
                        viewport[
                            "name"
                        ],
                    )


                    await render_zillow_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "rental_application",

                        template_name=
                            "rental_application.html",

                        context_key=
                            "rental",

                        page_data=
                            rental_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

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


if __name__ == "__main__":

    asyncio.run(
        main()
    )