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

from system.ios.generators.app_library_generator import (
    APP_LIBRARY_STATES,
    generate_app_library_data,
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


THEME_MODE = (
    "random"
)


STATE_MODE = (
    "random"
)


SELECTED_STATES = [

    "normal",
]


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
# Theme
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
# State
# ==========================================================

def resolve_state() -> str:

    if STATE_MODE == "random":

        return random.choice(
            APP_LIBRARY_STATES
        )


    if STATE_MODE == "selected":

        invalid = [

            state
            for state
            in SELECTED_STATES

            if state
            not in APP_LIBRARY_STATES
        ]


        if invalid:

            raise ValueError(
                f"Unknown states: {invalid}"
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


                    app_library = (
                        generate_app_library_data(

                            viewport=
                                viewport,

                            state=
                                state,
                        )
                    )


                    print(
                        "[APP LIBRARY]",
                        "sample=",
                        sample_index,
                        "viewport=",
                        viewport["name"],
                        "state=",
                        state,
                        "theme=",
                        theme_mode,
                    )


                    # ======================================
                    # IMPORTANT:
                    #
                    # One output directory for the page.
                    # State is encoded into page_type,
                    # therefore into the output filename.
                    # ======================================

                    await render_ios_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            f"app_library_{state}",

                        template_name=
                            "app_library.html",

                        context_key=
                            "app_library",

                        page_data=
                            app_library,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "app_library",

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            False,

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