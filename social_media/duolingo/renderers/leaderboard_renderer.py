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

from social_media.duolingo.generators.leaderboard_generator import (
    generate_leaderboard_data,
)

from social_media.duolingo.renderers.common_renderer import (
    render_duolingo_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
# SELECTED_VIEWPORTS = [
#     "small_mobile",
#     "small_laptop",
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
NUM_SAMPLES = 50
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
# Generate Theme
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

async def main():

    viewports = (
        get_viewports_by_names(
            SELECTED_VIEWPORTS
        )
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

                leaderboard_data = (
                    generate_leaderboard_data()
                )


                theme = (
                    generate_theme()
                )


                system = (
                    generate_system_data()
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    "DUOLINGO LEADERBOARD"
                )

                print(
                    "Sample:",
                    sample_index
                )

                print(
                    "League:",
                    leaderboard_data[
                        "league"
                    ][
                        "name"
                    ]
                )

                print(
                    "Theme:",
                    theme["mode"]
                )

                print(
                    "======================================"
                )


                for viewport in viewports:

                    print(
                        "Rendering:",
                        viewport["name"]
                    )


                    await render_duolingo_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "leaderboard",

                        template_name=
                            "leaderboard.html",

                        context_key=
                            "leaderboard",

                        page_data=
                            leaderboard_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "leaderboard",

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
# Entrypoint
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )