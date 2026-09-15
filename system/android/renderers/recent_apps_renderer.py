from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from android.generators.android_system_generator import (
    generate_android_system_data,
)

from android.generators.recent_apps_generator import (
    generate_recent_apps_data,
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
]


MIN_SCROLL_DELTA = 0


# ==========================================================
# Theme
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
# Viewports
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

async def render_recent_apps(
    browser,
    sample_index: int,
    recents: dict,
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
            "recent_apps",

        template_name=
            "recent_apps.html",

        context_key=
            "recents",

        page_data=
            recents,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "recent_apps",

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

                recents = (
                    generate_recent_apps_data()
                )

                system = (
                    generate_android_system_data()
                )


                # Modern Android first.
                system[
                    "navigation_mode"
                ] = random.choices(

                    [
                        "gesture",
                        "three_button",
                    ],

                    weights=[
                        0.85,
                        0.15,
                    ],

                    k=1,

                )[0]


                themes = (
                    resolve_themes()
                )


                print(
                    "\n"
                    "====================================="
                )

                print(
                    "RECENT APPS:",
                    sample_index,
                )

                print(
                    "State:",
                    recents[
                        "overview_state"
                    ],
                )

                print(
                    "Apps:",
                    recents[
                        "recent_count"
                    ],
                )

                print(
                    "Menu:",
                    recents[
                        "show_menu"
                    ],
                )

                print(
                    "Split:",
                    recents[
                        "show_split_suggestion"
                    ],
                )

                print(
                    "Layout:",
                    recents[
                        "layout_variant"
                    ],
                )

                print(
                    "Navigation:",
                    system[
                        "navigation_mode"
                    ],
                )


                for theme in themes:

                    for viewport in viewports:

                        await render_recent_apps(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            recents=
                                recents,

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