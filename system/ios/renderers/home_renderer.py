from __future__ import annotations

import asyncio
import random

from pathlib import Path

from playwright.async_api import (
    async_playwright,
)

from system.common.palette_generator import (
    generate_accessible_theme,
)

from system.common.viewport import (
    get_viewports_by_names,
)

from system.ios.generators.home_generator import (
    HOME_STATES,
    generate_home_data,
)

from system.ios.generators.system_generator import (
    generate_system_data_for_viewport,
)

from system.ios.renderers.renderer import (
    render_ios_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# SELECTED_VIEWPORTS = [
#
#     "small_mobile",
#
#     "standard_iphone",
#
#     "large_mobile",
#
#     "mobile_landscape",
#
#     "tablet_portrait",
#
#     "large_tablet_portrait",
#
#     "tablet_landscape",
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

# ANNOTATION_PROFILES = [
#
#     "big_components",
#
#     "components",
#
#     "small_elements",
#
#     "icons_only",
# ]
ANNOTATION_PROFILES = [

    "big_components",

    "small_elements",

]


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# State Configuration
# ==========================================================

STATE_MODE = "random"


SELECTED_STATES = [

    "normal",

    "folder_open",

    "context_menu",

    "edit_mode",

    "spotlight",

    "widget_edit",
]


# ==========================================================
# Capture Configuration
# ==========================================================

# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


# Home screen itself does not vertically scroll.
SCROLL_PERCENTAGES = [
    0,
]


MIN_VISIBLE_RATIO = 0.20


# ==========================================================
# Resolve Theme Mode
# ==========================================================

def resolve_theme_mode() -> str:

    if THEME_MODE == "random":

        return random.choice([
            "light",
            "dark",
        ])

    if THEME_MODE in {
        "light",
        "dark",
    }:

        return THEME_MODE

    raise ValueError(
        f"Unknown THEME_MODE: "
        f"{THEME_MODE}"
    )


# ==========================================================
# Resolve State
# ==========================================================

def resolve_state() -> str | None:

    if STATE_MODE == "random":

        return None

    if STATE_MODE == "selected":

        return random.choice(
            SELECTED_STATES
        )

    if STATE_MODE in HOME_STATES:

        return STATE_MODE

    raise ValueError(
        f"Unknown STATE_MODE: "
        f"{STATE_MODE}"
    )


# ==========================================================
# Render One Sample
# ==========================================================

async def render_home_sample(
    browser,
    sample_index: int,
    viewport: dict,
):

    theme_mode = (
        resolve_theme_mode()
    )


    # ======================================================
    # Theme
    # ======================================================

    theme = (
        generate_accessible_theme(
            mode=
                theme_mode
        )
    )


    # ======================================================
    # iOS System Chrome
    # ======================================================

    system = (
        generate_system_data_for_viewport(
            viewport
        )
    )


    # ======================================================
    # Home Screen
    # ======================================================

    requested_state = (
        resolve_state()
    )

    home = (
        generate_home_data(

            viewport=
                viewport,

            state=
                requested_state,
        )
    )


    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "[iOS HOME]"
    )

    print(
        "sample:",
        sample_index,
    )

    print(
        "viewport:",
        viewport["name"],
    )

    print(
        "state:",
        home["state"],
    )

    print(
        "theme:",
        theme["mode"],
    )


    # ======================================================
    # Render
    # ======================================================

    result = await render_ios_page(

        browser=
            browser,

        sample_index=
            sample_index,

        page_type=
            "home",

        template_name=
            "home_screen.html",

        context_key=
            "home",

        page_data=
            home,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "home",

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
    )


    return result


# ==========================================================
# Main
# ==========================================================

async def main():

    viewports = (
        get_viewports_by_names(
            SELECTED_VIEWPORTS
        )
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS HOME SCREEN DATASET"
    )

    print(
        "=========================================="
    )

    print(
        "Samples:",
        NUM_SAMPLES,
    )

    print(
        "Viewports:",
        [
            viewport["name"]
            for viewport
            in viewports
        ],
    )

    print(
        "Profiles:",
        ANNOTATION_PROFILES,
    )

    print(
        "State mode:",
        STATE_MODE,
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

                for viewport in viewports:

                    try:

                        await render_home_sample(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            viewport=
                                viewport,
                        )

                    except Exception as error:

                        print(
                            "\n"
                            "[iOS HOME ERROR]"
                        )

                        print(
                            "Sample:",
                            sample_index,
                        )

                        print(
                            "Viewport:",
                            viewport[
                                "name"
                            ],
                        )

                        print(
                            "Error:",
                            repr(
                                error
                            ),
                        )

                        raise

        finally:

            await browser.close()


    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS HOME GENERATION COMPLETE"
    )

    print(
        "=========================================="
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )