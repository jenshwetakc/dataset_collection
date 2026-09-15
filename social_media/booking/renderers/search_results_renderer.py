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

from social_media.booking.generators.search_results_generator import (
    generate_search_results_data,
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


# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
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
]


THEME_MODE = "random"


# ==========================================================
# Theme
# ==========================================================

def generate_theme():

    mode = (
        random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Main
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

                results_data = (
                    generate_search_results_data()
                )

                system = (
                    generate_system_data()
                )

                theme = (
                    generate_theme()
                )


                print(
                    "\n=============================="
                )

                print(
                    "SEARCH RESULTS SAMPLE:",
                    sample_index,
                )

                print(
                    "State:",
                    results_data[
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
                    "=============================="
                )


                for viewport in viewports:

                    await render_booking_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "search_results",

                        template_name=
                            "search_results.html",

                        context_key=
                            "results",

                        page_data=
                            results_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "search_results",

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
        render()
    )