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

from social_media.google_news.generators.for_you_generator import (
    generate_for_you_data,
)

from social_media.google_news.renderers.common_renderer import (
    render_google_news_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
# SELECTED_VIEWPORTS = [
#     "small_mobile",
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
# Theme Helper
# ==========================================================

def generate_theme() -> dict:

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
# Main
# ==========================================================

async def main():

    viewports = (
        get_viewports_by_names(
            SELECTED_VIEWPORTS
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

                print(
                    "\n"
                    "=========================================="
                )

                print(
                    "GOOGLE NEWS FOR YOU "
                    f"SAMPLE {sample_index + 1}/{NUM_SAMPLES}"
                )

                print(
                    "=========================================="
                )


                # ==========================================
                # Generate Page Data
                # ==========================================

                page_data = (
                    generate_for_you_data()
                )


                # ==========================================
                # Theme
                # ==========================================

                theme = (
                    generate_theme()
                )


                print(
                    "Theme:",
                    theme["mode"],
                    theme["seed"],
                )


                # ==========================================
                # Render Every Viewport
                # ==========================================

                for viewport in viewports:

                    system = (
                        generate_system_data()
                    )

                    print(
                        "Rendering:",
                        viewport["name"],
                        (
                            f'{viewport["width"]}'
                            "x"
                            f'{viewport["height"]}'
                        ),
                    )


                    await render_google_news_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "for_you",

                        template_name=
                            "for_you.html",

                        context_key=
                            "for_you",

                        page_data=
                            page_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "for_you",

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