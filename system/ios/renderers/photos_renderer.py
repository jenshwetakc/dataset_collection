from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from system.common.viewport import (
    get_viewports_by_names,
)

from system.common.palette_generator import (
    generate_theme,
)

from system.ios.generators.photos_generator import (
    PHOTOS_STATES,
    generate_photos_data,
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


# ==========================================================
# Viewports
# ==========================================================

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
# ==========================================================
# Annotation Profiles
# ==========================================================

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

THEME_MODE = (
    "random"
)

# Supported:
#
# light
# dark
# random


# ==========================================================
# State
# ==========================================================

STATE_MODE = (
    "random"
)

# Supported:
#
# random
# selected


SELECTED_STATES = [

    "library",
]


# ==========================================================
# Capture
# ==========================================================

# CAPTURE_FULL_PAGE = (
#     True
# )
CAPTURE_FULL_PAGE = (
    False
)


CAPTURE_VIEWPORTS = (
    True
)


SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Resolve Theme
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
        "THEME_MODE must be "
        "'light', 'dark', or 'random'"
    )


# ==========================================================
# Resolve State
# ==========================================================

def resolve_state() -> str:

    if STATE_MODE == "random":

        return random.choice(
            PHOTOS_STATES
        )


    if STATE_MODE == "selected":

        if not SELECTED_STATES:

            raise ValueError(
                "SELECTED_STATES cannot be empty "
                "when STATE_MODE='selected'"
            )


        invalid_states = [

            state

            for state
            in SELECTED_STATES

            if state
            not in PHOTOS_STATES
        ]


        if invalid_states:

            raise ValueError(

                f"Unknown Photos states: "
                f"{invalid_states}. "
                f"Available states: "
                f"{PHOTOS_STATES}"
            )


        return random.choice(
            SELECTED_STATES
        )


    raise ValueError(
        "STATE_MODE must be "
        "'random' or 'selected'"
    )


# ==========================================================
# Resolve Viewports
# ==========================================================

def resolve_ios_viewports() -> list[dict]:

    return get_viewports_by_names(
        SELECTED_VIEWPORTS
    )


# ==========================================================
# Debug
# ==========================================================

def print_configuration(
    viewports: list[dict],
) -> None:

    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS PHOTOS RENDERER"
    )

    print(
        "=========================================="
    )


    print(
        "samples:",
        NUM_SAMPLES,
    )


    print(
        "theme mode:",
        THEME_MODE,
    )


    print(
        "state mode:",
        STATE_MODE,
    )


    print(
        "output folder:",
        "photos",
    )


    print(
        "viewports:"
    )


    for viewport in viewports:

        print(

            "  -",

            viewport[
                "name"
            ],

            f"{viewport['width']}x"
            f"{viewport['height']}",

            viewport[
                "orientation"
            ],
        )


    print(
        "=========================================="
    )


# ==========================================================
# Main
# ==========================================================

async def main() -> None:

    # ======================================================
    # Viewports
    # ======================================================

    viewports = (
        resolve_ios_viewports()
    )


    print_configuration(
        viewports
    )


    # ======================================================
    # Playwright
    # ======================================================

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(

            headless=True
        )


        try:

            # ==============================================
            # Samples
            # ==============================================

            for sample_index in range(
                NUM_SAMPLES
            ):


                # ==========================================
                # Viewports
                # ==========================================

                for viewport in viewports:


                    # ======================================
                    # State
                    # ======================================

                    state = (
                        resolve_state()
                    )


                    # ======================================
                    # Theme
                    # ======================================

                    theme_mode = (
                        resolve_theme_mode()
                    )


                    theme = (
                        generate_theme(
                            mode=
                                theme_mode
                        )
                    )


                    # ======================================
                    # System
                    # ======================================

                    system = (
                        generate_system_data_for_viewport(
                            viewport
                        )
                    )


                    # ======================================
                    # Photos
                    # ======================================

                    photos = (
                        generate_photos_data(

                            viewport=
                                viewport,

                            state=
                                state,
                        )
                    )


                    # ======================================
                    # Debug
                    # ======================================

                    print(
                        "\n"
                        "------------------------------------------"
                    )


                    print(
                        "[PHOTOS]"
                    )


                    print(
                        "sample:",
                        sample_index,
                    )


                    print(
                        "viewport:",
                        viewport[
                            "name"
                        ],
                    )


                    print(
                        "state:",
                        state,
                    )


                    print(
                        "theme:",
                        theme_mode,
                    )


                    print(
                        "overlay:",
                        photos[
                            "is_overlay_state"
                        ],
                    )


                    # ======================================
                    # Render
                    # ======================================
                    #
                    # One output folder:
                    #
                    # output/photos/
                    #
                    # State goes into filename using
                    # page_type.
                    # ======================================

                    await render_ios_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            f"photos_{state}",

                        template_name=
                            "photos.html",

                        context_key=
                            "photos",

                        page_data=
                            photos,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "photos",

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
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )