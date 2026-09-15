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

from system.ios.generators.files_generator import (
    FILES_STATES,
    generate_files_data,
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

    "icons_only",
]


# ==========================================================
# Theme
# ==========================================================

THEME_MODE = (
    "random"
)


# ==========================================================
# State
# ==========================================================

STATE_MODE = (
    "random"
)


SELECTED_STATES = [

    "browse",
]


# ==========================================================
# Capture
# ==========================================================

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
        "THEME_MODE must be "
        "'light', 'dark', or 'random'"
    )


# ==========================================================
# State Resolver
# ==========================================================

def resolve_state() -> str:

    if STATE_MODE == "random":

        return random.choice(
            FILES_STATES
        )


    if STATE_MODE == "selected":

        if not SELECTED_STATES:

            raise ValueError(
                "SELECTED_STATES cannot be empty"
            )


        invalid_states = [

            state

            for state
            in SELECTED_STATES

            if state
            not in FILES_STATES
        ]


        if invalid_states:

            raise ValueError(
                f"Unknown Files states: "
                f"{invalid_states}"
            )


        return random.choice(
            SELECTED_STATES
        )


    raise ValueError(
        "STATE_MODE must be "
        "'random' or 'selected'"
    )


# ==========================================================
# Main
# ==========================================================

async def main() -> None:

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS FILES RENDERER"
    )

    print(
        "=========================================="
    )


    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(

            headless=True
        )


        try:

            for sample_index in range(
                NUM_SAMPLES
            ):


                for viewport in viewports:


                    state = (
                        resolve_state()
                    )


                    theme_mode = (
                        resolve_theme_mode()
                    )


                    theme = (
                        generate_theme(
                            mode=
                                theme_mode
                        )
                    )


                    system = (
                        generate_system_data_for_viewport(
                            viewport
                        )
                    )


                    files = (
                        generate_files_data(

                            viewport=
                                viewport,

                            state=
                                state,
                        )
                    )


                    print(

                        "[FILES]",

                        "sample=",
                        sample_index,

                        "viewport=",
                        viewport[
                            "name"
                        ],

                        "state=",
                        state,

                        "theme=",
                        theme_mode,
                    )


                    # ======================================
                    # One output directory:
                    #
                    # output/files/
                    #
                    # State encoded in page_type / filename.
                    # ======================================

                    await render_ios_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            f"files_{state}",

                        template_name=
                            "files.html",

                        context_key=
                            "files",

                        page_data=
                            files,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "files",

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