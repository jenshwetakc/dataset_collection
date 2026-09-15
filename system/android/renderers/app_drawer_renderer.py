from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from android.generators.android_system_generator import (
    generate_android_system_data,
)

from android.generators.app_drawer_generator import (
    generate_app_drawer_data,
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
# Dataset
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Annotation
# ==========================================================

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# ==========================================================
# Theme
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Viewports
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
# Render
# ==========================================================

async def render_app_drawer(
    browser,
    sample_index: int,
    drawer: dict,
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
            "app_drawer",

        template_name=
            "app_drawer.html",

        context_key=
            "drawer",

        page_data=
            drawer,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "app_drawer",

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

                drawer = (
                    generate_app_drawer_data()
                )

                system = (
                    generate_android_system_data()
                )


                # Modern Android should generally use gesture
                # navigation, with 3-button navigation retained
                # as a less-common alternate state.

                system[
                    "navigation_mode"
                ] = random.choices(
                    [
                        "gesture",
                        "three_button",
                    ],
                    weights=[
                        0.82,
                        0.18,
                    ],
                    k=1,
                )[0]


                themes = (
                    resolve_themes()
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    "APP DRAWER SAMPLE:",
                    sample_index,
                )

                print(
                    "State:",
                    drawer[
                        "drawer_state"
                    ],
                )

                print(
                    "Columns:",
                    drawer[
                        "columns"
                    ],
                )

                print(
                    "Tab:",
                    drawer[
                        "active_tab"
                    ],
                )

                print(
                    "Work profile:",
                    drawer[
                        "has_work_profile"
                    ],
                )

                print(
                    "Suggestions:",
                    drawer[
                        "show_suggestions"
                    ],
                )

                print(
                    "Keyboard:",
                    drawer[
                        "show_keyboard"
                    ],
                )

                print(
                    "Wallpaper:",
                    bool(
                        drawer[
                            "wallpaper"
                        ]
                    ),
                )

                print(
                    "Navigation:",
                    system[
                        "navigation_mode"
                    ],
                )


                for theme in themes:

                    for viewport in viewports:

                        await render_app_drawer(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            drawer=
                                drawer,

                            system=
                                system,

                            theme=
                                theme,

                            viewport=
                                viewport,
                        )


        finally:

            await browser.close()


if __name__ == "__main__":

    asyncio.run(
        main()
    )