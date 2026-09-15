# connectivity_expanded
# focus_picker
# media_expanded
# recording_active


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

from system.ios.generators.control_center_generator import (
    CONTROL_CENTER_STATES,
    generate_control_center_data,
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


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODE = (
    "random"
)

# Supported:
#
# "light"
# "dark"
# "random"


# ==========================================================
# State Configuration
# ==========================================================

STATE_MODE = (
    "random"
)

# Supported:
#
# "random"
# "selected"


SELECTED_STATES = [

    "normal",
]


# ==========================================================
# Capture Configuration
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
# Resolve State
# ==========================================================

def resolve_state() -> str:
    """
    Resolve the Control Center state.

    STATE_MODE:
        random
        selected
    """

    if STATE_MODE == "random":

        return random.choice(
            CONTROL_CENTER_STATES
        )


    if STATE_MODE == "selected":

        if not SELECTED_STATES:

            raise ValueError(
                "SELECTED_STATES cannot be empty "
                "when STATE_MODE='selected'"
            )


        invalid_states = [

            state
            for state in SELECTED_STATES
            if state
            not in CONTROL_CENTER_STATES
        ]


        if invalid_states:

            raise ValueError(

                "Unknown Control Center states: "
                f"{invalid_states}. "
                f"Available states: "
                f"{CONTROL_CENTER_STATES}"
            )


        return random.choice(
            SELECTED_STATES
        )


    raise ValueError(
        "STATE_MODE must be "
        "'random' or 'selected'"
    )


# ==========================================================
# Resolve Theme Mode
# ==========================================================

def resolve_theme_mode() -> str:
    """
    Resolve theme mode before calling generate_theme().

    generate_theme() itself only accepts:

        light
        dark

    Therefore "random" must be resolved here.
    """

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
# Resolve Viewports
# ==========================================================

def resolve_ios_viewports() -> list[dict]:
    """
    Resolve the configured iOS-compatible viewports.

    Uses the common viewport helper directly.
    """

    return get_viewports_by_names(
        SELECTED_VIEWPORTS
    )


# ==========================================================
# Debug Configuration
# ==========================================================

def print_configuration(
    viewports: list[dict],
) -> None:

    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS CONTROL CENTER RENDERER"
    )

    print(
        "=========================================="
    )


    print(
        "NUM_SAMPLES:",
        NUM_SAMPLES,
    )


    print(
        "THEME_MODE:",
        THEME_MODE,
    )


    print(
        "STATE_MODE:",
        STATE_MODE,
    )


    print(
        "CAPTURE_FULL_PAGE:",
        CAPTURE_FULL_PAGE,
    )


    print(
        "CAPTURE_VIEWPORTS:",
        CAPTURE_VIEWPORTS,
    )


    print(
        "SCROLL_PERCENTAGES:",
        SCROLL_PERCENTAGES,
    )


    print(
        "\nViewports:"
    )


    for viewport in viewports:

        print(
            "  -",
            viewport[
                "name"
            ],
            (
                viewport[
                    "width"
                ],
                viewport[
                    "height"
                ],
            ),
            viewport[
                "category"
            ],
        )


    print(
        "\nAvailable states:"
    )


    for state in CONTROL_CENTER_STATES:

        print(
            "  -",
            state,
        )


    print(
        "\n"
        "=========================================="
    )


# ==========================================================
# Main Renderer
# ==========================================================

async def main() -> None:

    # ======================================================
    # Resolve Viewports
    # ======================================================

    viewports = (
        resolve_ios_viewports()
    )


    # ======================================================
    # Debug
    # ======================================================

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
                    # Resolve State
                    # ======================================

                    state = (
                        resolve_state()
                    )


                    # ======================================
                    # Resolve Theme
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
                    # iOS System Data
                    # ======================================

                    system = (
                        generate_system_data_for_viewport(
                            viewport
                        )
                    )


                    # ======================================
                    # Control Center Data
                    # ======================================

                    control_center = (
                        generate_control_center_data(

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
                        "[CONTROL CENTER]"
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
                        f"{viewport['width']}x"
                        f"{viewport['height']}",
                    )


                    print(
                        "orientation:",
                        viewport[
                            "orientation"
                        ],
                    )


                    print(
                        "category:",
                        viewport[
                            "category"
                        ],
                    )


                    print(
                        "device_family:",
                        control_center[
                            "device_family"
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
                        control_center[
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
                            "control_center",

                        template_name=
                            "control_center.html",

                        context_key=
                            "control_center",

                        page_data=
                            control_center,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "control_center",

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

            # ==============================================
            # Always Close Browser
            # ==============================================

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )