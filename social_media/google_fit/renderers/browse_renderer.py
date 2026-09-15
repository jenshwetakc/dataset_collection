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

from social_media.google_fit.generators.browse_generator import (
    BROWSE_STATES,
    generate_browse_data,
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
# THEME_MODE = "both"
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

NUM_SAMPLES = 30
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
# State Mode
#
# random
# all
# selected
# ==========================================================

STATE_MODE = "random"


SELECTED_STATES = [
    "default",
    "search_active",
    "offline",
]


# ==========================================================
# State Resolver
# ==========================================================

def resolve_states() -> list[str]:

    if STATE_MODE == "random":

        return [
            random.choice(
                BROWSE_STATES
            )
        ]


    if STATE_MODE == "all":

        return list(
            BROWSE_STATES
        )


    if STATE_MODE == "selected":

        return list(
            SELECTED_STATES
        )


    raise ValueError(
        f"Unknown STATE_MODE: "
        f"{STATE_MODE}"
    )


# ==========================================================
# Theme Resolver
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


    return [
        THEME_MODE
    ]


# ==========================================================
# Render
# ==========================================================

async def render_browse():

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


                for state in (
                    resolve_states()
                ):

                    browse_data = (
                        generate_browse_data(
                            state=state
                        )
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


                            await render_google_fit_page(

                                browser=
                                    browser,

                                sample_index=
                                    sample_index,

                                page_type=
                                    f"browse_{state}",

                                template_name=
                                    "browse.html",

                                context_key=
                                    "browse",

                                page_data=
                                    browse_data,

                                system=
                                    system,

                                theme=
                                    theme,

                                viewport=
                                    viewport,

                                output_subdir=
                                    "browse",

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
        render_browse()
    )