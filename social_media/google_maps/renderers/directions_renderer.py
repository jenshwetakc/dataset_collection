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

from social_media.google_maps.generators.directions_generator import (
    generate_directions_data,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.google_maps.renderers.common_renderer import (
    render_google_maps_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     # "tablet_portrait",
#     # "laptop",
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
# # Directions is mostly viewport-fixed.
# SCROLL_PERCENTAGES = [
#     0,
# ]
NUM_SAMPLES = 25
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
    0
]


# ==========================================================
# Theme
# ==========================================================

def generate_page_theme() -> dict:

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

async def render_samples():

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
                1,
                NUM_SAMPLES + 1,
            ):

                directions_data = (
                    generate_directions_data()
                )

                system_data = (
                    generate_system_data()
                )

                for viewport in viewports:

                    theme = (
                        generate_page_theme()
                    )

                    await render_google_maps_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "directions",

                        template_name=
                            "directions.html",

                        context_key=
                            "directions",

                        page_data=
                            directions_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "directions",

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
        render_samples()
    )