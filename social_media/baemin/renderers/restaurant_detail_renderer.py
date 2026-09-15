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

from social_media.baemin.generators.restaurant_detail_generator import (
    generate_restaurant_detail_data,
)

from social_media.baemin.generators.system_generator import (
    generate_system_data,
)

from social_media.baemin.renderers.common_renderer import (
    render_baemin_page,
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Viewport
# ==========================================================

VIEWPORT_MODE = "selected"


# SELECTED_VIEWPORTS = [
#
#     "standard_iphone",
#     # "tablet_portrait",
#     # "laptop",
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

# ==========================================================
# Annotation Profiles
# ==========================================================

# ANNOTATION_PROFILES = [
#
#     "big_components",
#     # "components",
#     "small_elements",
#     # "icons_only",
# ]
ANNOTATION_PROFILES = [

    "big_components",
    "small_elements",
]


# ==========================================================
# Theme
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Capture
# ==========================================================

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


MIN_VISIBLE_RATIO = 0.20

MIN_SCROLL_DELTA = 100

SCROLL_SETTLE_MS = 150


# ==========================================================
# Theme Generator
# ==========================================================

def generate_page_theme() -> dict:

    if THEME_MODE == "random":

        mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

    else:

        mode = (
            THEME_MODE
        )


    return generate_accessible_theme(
        mode=mode
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

        browser = (
            await playwright.chromium.launch(
                headless=True
            )
        )


        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                # ==========================================
                # Generate Once Per Sample
                # ==========================================

                restaurant_detail_data = (
                    generate_restaurant_detail_data()
                )


                system_data = (
                    generate_system_data()
                )


                theme = (
                    generate_page_theme()
                )


                # ==========================================
                # Render Viewports
                # ==========================================

                for viewport in viewports:

                    await render_baemin_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "restaurant_detail",

                        template_name=
                            "restaurant_detail.html",

                        context_key=
                            "restaurant_detail",

                        page_data=
                            restaurant_detail_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "restaurant_detail",

                        annotation_profiles=
                            ANNOTATION_PROFILES,


                        # ==================================
                        # Full Page
                        # ==================================

                        capture_full_page=
                            CAPTURE_FULL_PAGE,


                        # ==================================
                        # Viewport
                        # ==================================

                        capture_viewports=
                            CAPTURE_VIEWPORTS,

                        scroll_percentages=
                            SCROLL_PERCENTAGES,


                        # ==================================
                        # Visibility / Scroll
                        # ==================================

                        min_visible_ratio=
                            MIN_VISIBLE_RATIO,

                        min_scroll_delta=
                            MIN_SCROLL_DELTA,

                        scroll_settle_ms=
                            SCROLL_SETTLE_MS,
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