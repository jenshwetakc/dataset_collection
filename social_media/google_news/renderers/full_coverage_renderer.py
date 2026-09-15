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

from social_media.google_news.generators.full_coverage_generator import (
    FULL_COVERAGE_STATES,
    generate_full_coverage_data,
)

from social_media.google_news.renderers.common_renderer import (
    render_google_news_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 2
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

STATE_MODE = "cycle"


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
# State
# ==========================================================

def get_state(
    sample_index: int,
) -> str | None:

    if STATE_MODE == "random":

        return None


    if STATE_MODE == "cycle":

        return FULL_COVERAGE_STATES[
            sample_index
            % len(
                FULL_COVERAGE_STATES
            )
        ]


    if STATE_MODE in FULL_COVERAGE_STATES:

        return STATE_MODE


    raise ValueError(
        f"Unknown STATE_MODE: {STATE_MODE}"
    )


# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:

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

        browser = (
            await playwright.chromium.launch(
                headless=True
            )
        )

        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                page_data = (
                    generate_full_coverage_data(
                        state=get_state(
                            sample_index
                        )
                    )
                )

                theme = (
                    generate_theme()
                )


                print(
                    "\n======================================="
                )

                print(
                    "GOOGLE NEWS FULL COVERAGE"
                )

                print(
                    "State:",
                    page_data["state"],
                )

                print(
                    "Theme:",
                    theme["mode"],
                )

                print(
                    "======================================="
                )


                for viewport in viewports:

                    system = (
                        generate_system_data()
                    )


                    await render_google_news_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "full_coverage",

                        template_name=
                            "full_coverage.html",

                        context_key=
                            "coverage",

                        page_data=
                            page_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir="full_coverage",
                            # (
                            #     "full_coverage/"
                            #     f'{page_data["state"]}'
                            # ),

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
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )