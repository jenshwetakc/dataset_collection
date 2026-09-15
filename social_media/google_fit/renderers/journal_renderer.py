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
    get_all_viewports,
    get_random_viewport,
    get_viewports_by_category,
    get_viewports_by_names,
    get_viewports_by_size_class,
)

from social_media.google_fit.generators.journal_generator import (
    generate_journal_data,
)

from social_media.google_fit.renderers.common_renderer import (
    render_google_fit_page,
)


# ==========================================================
# Configuration
# ==========================================================
#
# NUM_SAMPLES = 3
#
#
VIEWPORT_MODE = (
    "selected"
)
#
#
# SELECTED_VIEWPORTS = [
#     "small_mobile",
#     "laptop",
#     "desktop_fhd",
# ]
#
#
# THEME_MODE = (
#     "both"
# )
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
    0,
    25,
    50,
    75,
    100,
]

MIN_VISIBLE_RATIO = 0.20

MIN_SCROLL_DELTA = 100

SCROLL_SETTLE_MS = 150


# ==========================================================
# Viewports
# ==========================================================

def resolve_selected_viewports():

    if VIEWPORT_MODE == "all":

        return get_all_viewports()


    if VIEWPORT_MODE == "selected":

        return get_viewports_by_names(
            SELECTED_VIEWPORTS
        )


    if VIEWPORT_MODE == "random":

        return [
            get_random_viewport()
        ]


    if VIEWPORT_MODE in {
        "mobile",
        "mobile_landscape",
        "tablet",
        "foldable",
        "laptop",
        "desktop",
        "ultrawide",
    }:

        return get_viewports_by_category(
            VIEWPORT_MODE
        )


    if VIEWPORT_MODE in {
        "compact",
        "medium",
        "expanded",
    }:

        return get_viewports_by_size_class(
            VIEWPORT_MODE
        )


    raise ValueError(
        f"Unknown VIEWPORT_MODE: "
        f"{VIEWPORT_MODE}"
    )


# ==========================================================
# Theme
# ==========================================================

def resolve_theme_modes():

    if THEME_MODE == "both":

        return [
            "light",
            "dark",
        ]


    if THEME_MODE == "random":

        return [
            random.choice(
                [
                    "light",
                    "dark",
                ]
            )
        ]


    if THEME_MODE in {
        "light",
        "dark",
    }:

        return [
            THEME_MODE
        ]


    raise ValueError(
        f"Unknown THEME_MODE: "
        f"{THEME_MODE}"
    )


# ==========================================================
# Renderer
# ==========================================================

async def render_journal():

    viewports = (
        resolve_selected_viewports()
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

                journal_data = (
                    generate_journal_data()
                )


                for theme_mode in (
                    resolve_theme_modes()
                ):

                    theme = (
                        generate_accessible_theme(
                            mode=theme_mode
                        )
                    )


                    for viewport in (
                        viewports
                    ):

                        system = (
                            generate_system_data()
                        )


                        print(
                            "\n"
                            "======================================"
                        )

                        print(
                            "Google Fit Journal"
                        )

                        print(
                            "Sample:",
                            sample_index,
                        )

                        print(
                            "Theme:",
                            theme_mode,
                        )

                        print(
                            "Viewport:",
                            viewport[
                                "name"
                            ],
                        )

                        print(
                            "======================================"
                        )


                        await render_google_fit_page(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            page_type=
                                "journal",

                            template_name=
                                "journal.html",

                            context_key=
                                "journal",

                            page_data=
                                journal_data,

                            system=
                                system,

                            theme=
                                theme,

                            viewport=
                                viewport,

                            output_subdir=
                                "journal",

                            annotation_profiles=
                                ANNOTATION_PROFILES,

                            min_visible_ratio=
                                MIN_VISIBLE_RATIO,

                            capture_full_page=
                                CAPTURE_FULL_PAGE,

                            capture_viewports=
                                CAPTURE_VIEWPORTS,

                            scroll_percentages=
                                SCROLL_PERCENTAGES,

                            min_scroll_delta=
                                MIN_SCROLL_DELTA,

                            scroll_settle_ms=
                                SCROLL_SETTLE_MS,
                        )


        finally:

            await browser.close()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        render_journal()
    )