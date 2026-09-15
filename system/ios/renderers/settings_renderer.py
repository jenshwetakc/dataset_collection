from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from system.common.palette_generator import (
    generate_accessible_theme,
)

from system.common.viewport import (
    get_viewports_by_names,
)

from system.ios.generators.settings_generator import (
    SETTINGS_STATES,
    generate_settings_data,
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

NUM_SAMPLES = 60


# SELECTED_VIEWPORTS = [
#
#     "small_mobile",
#
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
# Theme
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# State
# ==========================================================

STATE_MODE = "random"


SELECTED_STATES = [

    "main",

    "search_active",

    "wifi",

    "bluetooth",

    "notifications",

    "appearance",

    "storage",

    "confirmation_dialog",
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


MIN_VISIBLE_RATIO = 0.20


# ==========================================================
# Theme Resolver
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
# State Resolver
# ==========================================================

def resolve_state() -> str | None:

    if STATE_MODE == "random":

        return None

    if STATE_MODE == "selected":

        return random.choice(
            SELECTED_STATES
        )

    if STATE_MODE in SETTINGS_STATES:

        return STATE_MODE

    raise ValueError(
        f"Unknown STATE_MODE: "
        f"{STATE_MODE}"
    )


# ==========================================================
# Render Sample
# ==========================================================

async def render_settings_sample(
    browser,
    sample_index: int,
    viewport: dict,
):

    # ======================================================
    # Theme
    # ======================================================

    theme = (
        generate_accessible_theme(
            mode=
                resolve_theme_mode()
        )
    )


    # ======================================================
    # iOS System
    # ======================================================

    system = (
        generate_system_data_for_viewport(
            viewport
        )
    )


    # ======================================================
    # Settings
    # ======================================================

    settings = (
        generate_settings_data(

            viewport=
                viewport,

            state=
                resolve_state(),
        )
    )


    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "[iOS SETTINGS]"
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
        settings["state"],
    )

    print(
        "theme:",
        theme["mode"],
    )


    return await render_ios_page(

        browser=
            browser,

        sample_index=
            sample_index,

        page_type=
            "settings",

        template_name=
            "settings.html",

        context_key=
            "settings",

        page_data=
            settings,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "settings",

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
        "iOS SETTINGS DATASET"
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
        "States:",
        SETTINGS_STATES,
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

                        await render_settings_sample(

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
                            "[iOS SETTINGS ERROR]"
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
        "iOS SETTINGS GENERATION COMPLETE"
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