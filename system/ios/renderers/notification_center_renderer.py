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

from system.ios.generators.notification_center_generator import (
    NOTIFICATION_CENTER_STATES,
    generate_notification_center_data,
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
            NOTIFICATION_CENTER_STATES
        )


    if STATE_MODE == "selected":

        if not SELECTED_STATES:

            raise ValueError(
                "SELECTED_STATES cannot be empty."
            )


        invalid = [

            state
            for state
            in SELECTED_STATES

            if state
            not in NOTIFICATION_CENTER_STATES
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
# Resolve Viewports
# ==========================================================

def resolve_ios_viewports() -> list[dict]:

    return get_viewports_by_names(
        SELECTED_VIEWPORTS
    )


# ==========================================================
# Main
# ==========================================================

async def main() -> None:

    viewports = (
        resolve_ios_viewports()
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS NOTIFICATION CENTER"
    )

    print(
        "=========================================="
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
        "States:",
        NOTIFICATION_CENTER_STATES,
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
                    # Page Data
                    # ======================================

                    notification_center = (
                        generate_notification_center_data(

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
                        "[NOTIFICATION CENTER]"
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
                        "size:",
                        (
                            viewport[
                                "width"
                            ],
                            viewport[
                                "height"
                            ],
                        ),
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
                        notification_center[
                            "is_overlay_state"
                        ],
                    )


                    # ======================================
                    # Render
                    # ======================================

                    await render_ios_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "notification_center",

                        template_name=
                            "notification_center.html",

                        context_key=
                            "notification_center",

                        page_data=
                            notification_center,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "notification_center",

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