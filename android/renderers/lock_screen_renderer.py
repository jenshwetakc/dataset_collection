from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from android.generators.android_system_generator import (
    generate_android_system_data,
)

from android.generators.lock_screen_generator import (
    generate_lock_screen_data,
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

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Viewport Configuration
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
# Capture
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
# Render One Lock Screen
# ==========================================================

async def render_lock_screen(
    browser,
    sample_index: int,
    lock: dict,
    system: dict,
    theme: dict,
    viewport: dict,
):

    return await render_android_page(

        browser=
            browser,

        sample_index=
            sample_index,

        page_type=
            "lock_screen",

        template_name=
            "lock_screen.html",

        context_key=
            "lock",

        page_data=
            lock,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "lock_screen",

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
        "ANDROID LOCK SCREEN DATASET"
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
        "Annotation profiles:",
        ANNOTATION_PROFILES,
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
                # Generate one logical lock-screen state
                # ==========================================

                lock = (
                    generate_lock_screen_data()
                )

                system = (
                    generate_android_system_data()
                )

                themes = (
                    resolve_themes()
                )


                # ==========================================
                # Debug
                # ==========================================

                print(
                    "\n"
                    "------------------------------------------"
                )

                print(
                    "Sample:",
                    sample_index,
                )

                print(
                    "Wallpaper:",
                    lock[
                        "wallpaper"
                    ][
                        "name"
                    ],
                )

                print(
                    "Notifications:",
                    lock[
                        "notification_count"
                    ],
                )

                print(
                    "Media:",
                    lock[
                        "show_media"
                    ],
                )

                print(
                    "Charging:",
                    lock[
                        "charging"
                    ],
                )

                print(
                    "Low battery:",
                    lock[
                        "low_battery"
                    ],
                )

                print(
                    "Unlock:",
                    lock[
                        "unlock"
                    ][
                        "method"
                    ],
                )


                # ==========================================
                # Render
                # ==========================================

                for theme in themes:

                    for viewport in viewports:

                        print(
                            "Rendering | "
                            f"{theme['mode']} | "
                            f"{viewport['name']}"
                        )


                        await render_lock_screen(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            lock=
                                lock,

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