from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.paypal.generators.system_generator import (
    generate_system_data,
)

from social_media.paypal.generators.home_generator import (
    generate_home_data,
)

from social_media.paypal.renderers.common_renderer import (
    render_paypal_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 5
#
#
# VIEWPORTS = [
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
#
#
# CAPTURE_FULL_PAGE = True
#
# CAPTURE_VIEWPORTS = True
#
#
# SCROLL_PERCENTAGES = [
#     0,
#     10,
#     20,
#     30,
#     40,
#     50,
#     60,
#     70,
#     80,
#     90,
#     100,
# ]
NUM_SAMPLES = 18
VIEWPORTS = [
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
        mode=mode,
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    selected_viewports = (
        get_viewports_by_names(
            VIEWPORTS
        )
    )

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                # ------------------------------------------
                # Data
                # ------------------------------------------

                home = (
                    generate_home_data()
                )


                # ------------------------------------------
                # Theme
                # ------------------------------------------

                theme = (
                    generate_theme()
                )


                # ------------------------------------------
                # System
                # ------------------------------------------

                system = (
                    generate_system_data()
                )


                # ------------------------------------------
                # Viewports
                # ------------------------------------------

                for viewport in (
                    selected_viewports
                ):

                    print(
                        "\n"
                        "========================================"
                    )

                    print(
                        "PayPal Home"
                    )

                    print(
                        "Sample:",
                        sample_index
                    )

                    print(
                        "Viewport:",
                        viewport["name"]
                    )

                    print(
                        "Theme:",
                        theme["mode"]
                    )

                    print(
                        "========================================"
                    )


                    await render_paypal_page(

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
                            home,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "home",

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
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )