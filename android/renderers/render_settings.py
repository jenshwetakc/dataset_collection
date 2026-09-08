from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from android.generators.android_system_generator import (
    generate_android_system_data,
)

from android.generators.settings_generator import (
    generate_settings_data,
)

from android.renderers.settings_renderer import (
    render_settings_page,
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

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# ==========================================================
# Theme Configuration
#
# Supported:
#
# "light"
# "dark"
# "random"
# "both"
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Viewport Configuration
#
# Supported modes:
#
# "all"
# "selected"
# "random"
# "mobile"
# "mobile_landscape"
# "tablet"
# "foldable"
# "compact"
# "medium"
# "expanded"
# "portrait"
# "landscape"
# ==========================================================

VIEWPORT_MODE = "selected"


# SELECTED_VIEWPORTS = [
#     "standard_android",
#     "large_mobile",
#     "tablet_portrait",
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


MIN_SCROLL_DELTA = 80


# ==========================================================
# Theme Resolver
# ==========================================================

def resolve_themes() -> list[dict]:
    """
    Resolve themes according to THEME_MODE.
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

        return [
            generate_accessible_theme(
                mode=random.choice([
                    "light",
                    "dark",
                ])
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
        f"{THEME_MODE}"
    )


# ==========================================================
# Viewport Resolver
# ==========================================================

def resolve_android_viewports() -> list[dict]:
    """
    Resolve Android viewports according to VIEWPORT_MODE.
    """

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
# Main
# ==========================================================

async def main():

    viewports = (
        resolve_android_viewports()
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "ANDROID SETTINGS DATASET"
    )

    print(
        "=========================================="
    )

    print(
        "Samples:",
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
            viewport["name"]
            for viewport in viewports
        ],
    )

    print(
        "Annotation profiles:",
        ANNOTATION_PROFILES,
    )

    print(
        "Capture full page:",
        CAPTURE_FULL_PAGE,
    )

    print(
        "Capture viewports:",
        CAPTURE_VIEWPORTS,
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
                # Generate logical state once per sample
                # ==========================================

                settings = (
                    generate_settings_data()
                )

                system = (
                    generate_android_system_data()
                )


                # ==========================================
                # Resolve theme(s)
                # ==========================================

                themes = (
                    resolve_themes()
                )


                for theme in themes:

                    for viewport in viewports:

                        print(
                            "\n"
                            "--------------------------------------"
                        )

                        print(
                            "Sample:",
                            sample_index,
                        )

                        print(
                            "Theme:",
                            theme["mode"],
                        )

                        print(
                            "Viewport:",
                            viewport["name"],
                        )

                        print(
                            "Size:",
                            f"{viewport['width']}x"
                            f"{viewport['height']}",
                        )

                        print(
                            "Wi-Fi:",
                            settings["state"][
                                "wifi_enabled"
                            ],
                        )

                        print(
                            "Bluetooth:",
                            settings["state"][
                                "bluetooth_enabled"
                            ],
                        )

                        print(
                            "Search expanded:",
                            settings[
                                "search_expanded"
                            ],
                        )


                        await render_settings_page(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            settings=
                                settings,

                            system=
                                system,

                            theme=
                                theme,

                            viewport=
                                viewport,

                            annotation_profiles=
                                ANNOTATION_PROFILES,

                            capture_full_page=
                                CAPTURE_FULL_PAGE,

                            capture_viewports=
                                CAPTURE_VIEWPORTS,

                            scroll_percentages=
                                SCROLL_PERCENTAGES,

                            min_scroll_delta=
                                MIN_SCROLL_DELTA,
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