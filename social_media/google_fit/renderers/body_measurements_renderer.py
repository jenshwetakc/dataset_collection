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
    get_viewports_by_orientation,
    get_viewports_by_size_class,
)

from social_media.google_fit.generators.body_measurements_generator import (
    BODY_MEASUREMENT_STATES,
    generate_body_measurements_data,
)

from social_media.google_fit.renderers.common_renderer import (
    render_google_fit_page,
)


# ==========================================================
# Samples
# ==========================================================
#
# NUM_SAMPLES = 2
#
#
# # ==========================================================
# # Viewport
# # ==========================================================
#
VIEWPORT_MODE = "selected"
#
#
# SELECTED_VIEWPORTS = [
#     "small_mobile",
#     "desktop_fhd",
# ]
#
#
# # ==========================================================
# # State
# #
# # all
# # random
# # selected
# # ==========================================================
#
STATE_MODE = "all"
#
#
SELECTED_STATES = [
    "normal",
    "add_measurement",
    "validation_error",
]
#
#
# # ==========================================================
# # Theme
# # ==========================================================
#
# THEME_MODE = "both"
#
#
# # ==========================================================
# # Annotation
# # ==========================================================
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
# ]
#
#
# # ==========================================================
# # Capture
# # ==========================================================
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

MIN_VISIBLE_RATIO = 0.20

MIN_SCROLL_DELTA = 100

SCROLL_SETTLE_MS = 150


# ==========================================================
# State Resolver
# ==========================================================

def resolve_states() -> list[str]:

    if STATE_MODE == "all":

        return list(
            BODY_MEASUREMENT_STATES
        )


    if STATE_MODE == "random":

        return [
            random.choice(
                BODY_MEASUREMENT_STATES
            )
        ]


    if STATE_MODE == "selected":

        invalid = (
            set(
                SELECTED_STATES
            )
            - set(
                BODY_MEASUREMENT_STATES
            )
        )

        if invalid:

            raise ValueError(
                f"Unknown body measurement states: "
                f"{sorted(invalid)}"
            )

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

def resolve_theme_modes() -> list[str]:

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
# Viewport Resolver
# ==========================================================

def resolve_selected_viewports():

    if VIEWPORT_MODE == "all":

        return get_all_viewports()


    if VIEWPORT_MODE == "random":

        return [
            get_random_viewport()
        ]


    if VIEWPORT_MODE == "selected":

        return get_viewports_by_names(
            SELECTED_VIEWPORTS
        )


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


    if VIEWPORT_MODE in {
        "portrait",
        "landscape",
    }:

        return get_viewports_by_orientation(
            VIEWPORT_MODE
        )


    raise ValueError(
        f"Unknown VIEWPORT_MODE: "
        f"{VIEWPORT_MODE}"
    )


# ==========================================================
# Renderer
# ==========================================================

async def render_body_measurements():

    viewports = (
        resolve_selected_viewports()
    )

    states = (
        resolve_states()
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

                for state in states:

                    body_data = (
                        generate_body_measurements_data(
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


                        for viewport in viewports:

                            system = (
                                generate_system_data()
                            )


                            print(
                                "\n"
                                "========================================"
                            )

                            print(
                                "Google Fit Body Measurements"
                            )

                            print(
                                "Sample:",
                                sample_index,
                            )

                            print(
                                "State:",
                                state,
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
                                "========================================"
                            )


                            await render_google_fit_page(

                                browser=
                                    browser,

                                sample_index=
                                    sample_index,

                                page_type=
                                    (
                                        f"body_measurements_"
                                        f"{state}"
                                    ),

                                template_name=
                                    "body_measurements.html",

                                context_key=
                                    "body",

                                page_data=
                                    body_data,

                                system=
                                    system,

                                theme=
                                    theme,

                                viewport=
                                    viewport,

                                output_subdir=
                                    "body_measurements",

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
        render_body_measurements()
    )