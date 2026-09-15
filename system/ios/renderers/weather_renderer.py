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

from system.ios.generators.weather_generator import (
    WEATHER_STATES,
    generate_weather_data,
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


# ==========================================================
# State
# ==========================================================

STATE_MODE = (
    "random"
)


SELECTED_STATES = [

    "current_weather",
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
            WEATHER_STATES
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
            not in WEATHER_STATES
        ]


        if invalid_states:

            raise ValueError(
                f"Unknown Weather states: "
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
        "iOS WEATHER RENDERER"
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
                    # Weather
                    # ======================================

                    weather = (
                        generate_weather_data(

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

                        "[WEATHER]",

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
                    # Render
                    #
                    # All states:
                    #
                    # output/weather/
                    #
                    # State encoded in filename/page_type.
                    # ======================================

                    await render_ios_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            f"weather_{state}",

                        template_name=
                            "weather.html",

                        context_key=
                            "weather",

                        page_data=
                            weather,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "weather",

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