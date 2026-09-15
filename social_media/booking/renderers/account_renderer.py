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

from social_media.booking.generators.account_generator import (
    generate_account_data,
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

                # Generate ONCE.
                # Same state/data across all viewports.

                account_data = (
                    generate_account_data()
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
                    "BOOKING ACCOUNT:",
                    sample_index,
                )

                print(
                    "State:",
                    account_data[
                        "state"
                    ],
                )

                print(
                    "======================================"
                )


                for viewport in viewports:

                    await render_booking_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "account",

                        template_name=
                            "account.html",

                        context_key=
                            "account",

                        page_data=
                            account_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "account",

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