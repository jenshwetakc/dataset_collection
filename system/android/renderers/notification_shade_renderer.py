from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from android.generators.android_system_generator import (
    generate_android_system_data,
)

from android.generators.notification_shade_generator import (
    generate_notification_shade_data,
)

from android.renderers.common_renderer import (
    render_android_page,
)

from common.palette_generator import (
    generate_accessible_theme,
)

from common.viewport import (
    get_all_viewports,
    get_random_viewport,
    get_viewports_by_category,
    get_viewports_by_names,
    get_viewports_by_orientation,
    get_viewports_by_size_class,
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Annotation Profiles
# ==========================================================
#
# We generate two annotation styles:
#
# 1. big_components
# 2. small_elements
#
# ==========================================================

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# ==========================================================
# Theme Configuration
# ==========================================================
#
# Supported:
#
# "light"
# "dark"
# "random"
# "both"
#
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Viewport Configuration
# ==========================================================
#
# Supported modes:
#
# "all"
# "selected"
# "random"
#
# Categories:
# "mobile"
# "mobile_landscape"
# "tablet"
# "foldable"
# "laptop"
# "desktop"
# "ultrawide"
#
# Size classes:
# "compact"
# "medium"
# "expanded"
#
# Orientation:
# "portrait"
# "landscape"
#
# ==========================================================

VIEWPORT_MODE = "selected"


# SELECTED_VIEWPORTS = [
#     "standard_android",
#     "foldable",
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
# Capture Configuration
# ==========================================================
#
# Notification shade is a mostly fixed Android system page,
# therefore we only need scroll position 0.
#
# ==========================================================

# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
]


MIN_SCROLL_DELTA = 0


# ==========================================================
# Theme Resolver
# ==========================================================

def resolve_themes() -> list[dict]:
    """
    Resolve themes according to THEME_MODE.

    random:
        One randomly selected light/dark theme per sample.

    both:
        Render both light and dark versions of the same
        generated logical UI state.
    """

    if THEME_MODE == "light":

        return [
            generate_accessible_theme(
                mode="light"
            )
        ]


    if THEME_MODE == "dark":

        return [
            generate_accessible_theme(
                mode="dark"
            )
        ]


    if THEME_MODE == "random":

        selected_mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

        return [
            generate_accessible_theme(
                mode=selected_mode
            )
        ]


    if THEME_MODE == "both":

        return [
            generate_accessible_theme(
                mode="light"
            ),

            generate_accessible_theme(
                mode="dark"
            ),
        ]


    raise ValueError(
        f"Unknown THEME_MODE: "
        f"{THEME_MODE}. "
        f"Expected one of: "
        f"light, dark, random, both."
    )


# ==========================================================
# Viewport Resolver
# ==========================================================

def resolve_android_viewports() -> list[dict]:
    """
    Resolve viewports according to VIEWPORT_MODE.
    """

    # ------------------------------------------------------
    # All
    # ------------------------------------------------------

    if VIEWPORT_MODE == "all":

        return get_all_viewports()


    # ------------------------------------------------------
    # Selected
    # ------------------------------------------------------

    if VIEWPORT_MODE == "selected":

        return get_viewports_by_names(
            SELECTED_VIEWPORTS
        )


    # ------------------------------------------------------
    # Random
    # ------------------------------------------------------

    if VIEWPORT_MODE == "random":

        return [
            get_random_viewport()
        ]


    # ------------------------------------------------------
    # Category
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Size Class
    # ------------------------------------------------------

    if VIEWPORT_MODE in {
        "compact",
        "medium",
        "expanded",
    }:

        return get_viewports_by_size_class(
            VIEWPORT_MODE
        )


    # ------------------------------------------------------
    # Orientation
    # ------------------------------------------------------

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
# Render One Notification Shade
# ==========================================================

async def render_notification_shade(
    browser,
    sample_index: int,
    shade: dict,
    system: dict,
    theme: dict,
    viewport: dict,
):
    """
    Render one notification shade UI.

    Actual screenshot/annotation logic is delegated to:

        system/android/renderers/common_renderer.py

    which itself delegates to:

        system/common/common_renderer.py
    """

    return await render_android_page(

        # --------------------------------------------------
        # Browser
        # --------------------------------------------------

        browser=
            browser,


        # --------------------------------------------------
        # Sample
        # --------------------------------------------------

        sample_index=
            sample_index,


        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        page_type=
            "notification_shade",

        template_name=
            "notification_shade.html",

        context_key=
            "shade",

        page_data=
            shade,


        # --------------------------------------------------
        # Global UI State
        # --------------------------------------------------

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,


        # --------------------------------------------------
        # Output
        # --------------------------------------------------

        output_subdir=
            "notification_shade",


        # --------------------------------------------------
        # Annotation
        # --------------------------------------------------

        annotation_profiles=
            ANNOTATION_PROFILES,


        # --------------------------------------------------
        # Capture
        # --------------------------------------------------

        capture_full_page=
            CAPTURE_FULL_PAGE,

        capture_viewports=
            CAPTURE_VIEWPORTS,


        # --------------------------------------------------
        # Scroll
        # --------------------------------------------------

        scroll_percentages=
            SCROLL_PERCENTAGES,

        min_scroll_delta=
            MIN_SCROLL_DELTA,
    )


# ==========================================================
# Debug State
# ==========================================================

def print_sample_state(
    *,
    sample_index: int,
    shade: dict,
    system: dict,
) -> None:

    print(
        "\n"
        "=========================================="
    )

    print(
        f"ANDROID NOTIFICATION SHADE "
        f"SAMPLE {sample_index}"
    )

    print(
        "=========================================="
    )

    print(
        "Shade state:",
        shade[
            "shade_state"
        ],
    )

    print(
        "Notification count:",
        shade[
            "notification_count"
        ],
    )

    print(
        "Show brightness:",
        shade[
            "show_brightness"
        ],
    )

    print(
        "Show media:",
        shade[
            "show_media"
        ],
    )

    print(
        "Navigation mode:",
        get(
            "navigation_mode"
        ),
    )


    controls = shade.get(
        "controls",
        {}
    )

    print(
        "Wi-Fi:",
        controls.get(
            "wifi"
        ),
    )

    print(
        "Bluetooth:",
        controls.get(
            "bluetooth"
        ),
    )

    print(
        "Airplane mode:",
        controls.get(
            "airplane_mode"
        ),
    )

    print(
        "Battery saver:",
        controls.get(
            "battery_saver"
        ),
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Resolve Viewports Once
    # ======================================================

    viewports = (
        resolve_android_viewports()
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "ANDROID NOTIFICATION SHADE DATASET"
    )

    print(
        "=========================================="
    )


    print(
        "Number of samples:",
        NUM_SAMPLES,
    )

    print(
        "Theme mode:",
        THEME_MODE,
    )

    print(
        "Viewport mode:",
        VIEWPORT_MODE,
    )

    print(
        "Selected viewports:",
        [
            viewport[
                "name"
            ]
            for viewport
            in viewports
        ],
    )

    print(
        "Annotation profiles:",
        ANNOTATION_PROFILES,
    )

    print(
        "Full page capture:",
        CAPTURE_FULL_PAGE,
    )

    print(
        "Viewport capture:",
        CAPTURE_VIEWPORTS,
    )


    # ======================================================
    # Playwright
    # ======================================================

    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch(
                headless=True
            )
        )


        try:

            # ==================================================
            # Samples
            # ==================================================

            for sample_index in range(
                NUM_SAMPLES
            ):

                # ==============================================
                # Generate Logical UI State
                #
                # IMPORTANT:
                #
                # Generate once here so that the same logical
                # notification shade can be rendered across
                # multiple themes and viewports.
                # ==============================================

                shade = (
                    generate_notification_shade_data()
                )

                system = (
                    generate_android_system_data()
                )


                # ==============================================
                # Resolve Theme(s)
                # ==============================================

                themes = (
                    resolve_themes()
                )


                # ==============================================
                # Debug
                # ==============================================

                print_sample_state(

                    sample_index=
                        sample_index,

                    shade=
                        shade,

                    system=
                        system,
                )


                # ==============================================
                # Themes
                # ==============================================

                for theme in themes:


                    # ==========================================
                    # Viewports
                    # ==========================================

                    for viewport in viewports:

                        print(
                            "\n"
                            "------------------------------------------"
                        )

                        print(
                            "Rendering:"
                        )

                        print(
                            "Sample:",
                            sample_index,
                        )

                        print(
                            "Theme:",
                            theme[
                                "mode"
                            ],
                        )

                        print(
                            "Viewport:",
                            viewport[
                                "name"
                            ],
                        )

                        print(
                            "Dimensions:",
                            f"{viewport['width']}"
                            f"x"
                            f"{viewport['height']}",
                        )

                        print(
                            "DPR:",
                            viewport.get(
                                "dpr",
                                1,
                            ),
                        )


                        # ======================================
                        # Render
                        # ======================================

                        await render_notification_shade(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            shade=
                                shade,

                            system=
                                system,

                            theme=
                                theme,

                            viewport=
                                viewport,
                        )


        finally:

            await browser.close()


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )