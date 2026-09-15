from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from tqdm import tqdm

from social_media.youtube.renderers.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.youtube.generators.shorts_camera_generator import (
    SHORTS_CAMERA_STATES,
    generate_shorts_camera_page,
)


# ==========================================================
# Paths
# ==========================================================

YOUTUBE_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = (
    YOUTUBE_ROOT
    / "templates"
)

OUTPUT_ROOT = (
    YOUTUBE_ROOT
    / "output"
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Camera States
# ==========================================================

CAMERA_STATES_TO_RENDER = [
    "idle",
    "recording",
    "paused",
    "countdown",
    "recorded",
    "effects_open",
]


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODES = [
    "light",
    "dark",
]


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORT_MODE = "selected"

SELECTED_VIEWPORTS = [
    "standard_iphone",
    "tablet_landscape",
    "laptop",
    "desktop_fhd",
]


# ==========================================================
# Scroll Configuration
# ==========================================================

# This is a fixed camera/editor-style screen.
# We do not need document scrolling.

SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = False

SAVE_VIEWPORTS = True


# ==========================================================
# Validate States
# ==========================================================

def validate_camera_states() -> None:

    unknown_states = [
        state
        for state in CAMERA_STATES_TO_RENDER
        if state not in SHORTS_CAMERA_STATES
    ]

    if unknown_states:

        raise ValueError(
            "Unknown Shorts camera states: "
            f"{unknown_states}. "
            f"Available states: "
            f"{SHORTS_CAMERA_STATES}"
        )


# ==========================================================
# Debug
# ==========================================================

def print_page_debug(
    page: dict,
) -> None:

    print(
        f"State: "
        f"{page['state']}"
    )

    print(
        f"Camera: "
        f"{page['preview']['camera']}"
    )

    print(
        f"Flash: "
        f"{page['preview']['flash']}"
    )

    print(
        f"Maximum duration: "
        f"{page['duration']['max_text']}"
    )

    print(
        f"Recording: "
        f"{page['recording']['is_recording']}"
    )

    print(
        f"Paused: "
        f"{page['recording']['is_paused']}"
    )

    print(
        f"Has recording: "
        f"{page['recording']['has_recording']}"
    )

    print(
        f"Segments: "
        f"{len(page['segments']['segments'])}"
    )

    print(
        f"Recorded percent: "
        f"{page['segments']['recorded_percent']}%"
    )

    print(
        f"Countdown: "
        f"{page['countdown']['enabled']}"
    )

    print(
        f"Effects open: "
        f"{page['effects']['open']}"
    )

    print(
        f"Sound: "
        f"{page['sound']['title']}"
    )

    print(
        f"Speed: "
        f"{page['speed']['selected']}"
    )

    print(
        "Tools:"
    )

    for tool in page["tools"]:

        print(
            f"  - "
            f"{tool['label']}"
            f" | "
            f"value={tool['value']}"
            f" | "
            f"selected={tool['selected']}"
        )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validate Configuration
    # ======================================================

    validate_camera_states()


    # ======================================================
    # Resolve Viewports
    # ======================================================

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Debug Configuration
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE SHORTS CAMERA"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )

    print(
        f"Camera states: "
        f"{CAMERA_STATES_TO_RENDER}"
    )

    print(
        f"Themes: "
        f"{THEME_MODES}"
    )

    print(
        f"Save full page: "
        f"{SAVE_FULL_PAGE}"
    )

    print(
        f"Save viewport: "
        f"{SAVE_VIEWPORTS}"
    )

    print(
        f"Scroll positions: "
        f"{SCROLL_PERCENTAGES}"
    )

    print(
        "\nTesting viewports:"
    )

    for viewport in viewports:

        orientation = (
            "landscape"
            if viewport["width"] > viewport["height"]
            else "portrait"
        )

        print(
            f"  - "
            f"{viewport['name']}"
            f" | "
            f"{viewport['width']}"
            f"x"
            f"{viewport['height']}"
            f" | "
            f"{orientation}"
            f" | "
            f"DPR="
            f"{viewport.get('dpr', 1)}"
        )


    # ======================================================
    # Playwright
    # ======================================================

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )


        # ==================================================
        # Sample Loop
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Shorts Camera",
        ):

            print(
                "\n"
                "------------------------------------------"
            )

            print(
                f"Sample: "
                f"{sample_index}"
            )


            # ==============================================
            # State Loop
            # ==============================================

            for camera_state in CAMERA_STATES_TO_RENDER:

                # ==========================================
                # Generate this state ONCE
                #
                # Important:
                # This exact same state/content is reused
                # across light/dark and every viewport.
                # ==========================================

                camera_page = (
                    generate_shorts_camera_page(
                        state=camera_state
                    )
                )


                print(
                    "\n"
                    "======================================"
                )

                print_page_debug(
                    camera_page
                )


                # ==========================================
                # Theme Loop
                # ==========================================

                for theme_mode in THEME_MODES:

                    theme = (
                        generate_accessible_theme(
                            mode=theme_mode
                        )
                    )


                    print(
                        "\n"
                        f"Theme: "
                        f"{theme_mode}"
                    )

                    print(
                        f"Seed: "
                        f"{theme.get('seed')}"
                    )

                    print(
                        f"WCAG pass: "
                        f"{theme.get('wcag_pass')}"
                    )


                    # ======================================
                    # Viewport Loop
                    # ======================================

                    for viewport in viewports:

                        print(
                            "Rendering: "
                            f"{camera_state}"
                            f" | "
                            f"{theme_mode}"
                            f" | "
                            f"{viewport['name']}"
                            f" "
                            f"("
                            f"{viewport['width']}"
                            f"x"
                            f"{viewport['height']}"
                            f")"
                        )


                        await render_page(

                            # ==============================
                            # Browser
                            # ==============================

                            browser=browser,


                            # ==============================
                            # Sample
                            # ==============================

                            sample_index=sample_index,

                            page_type="shorts_camera",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=(
                                "pages/shorts_camera.html"
                            ),

                            context_key="page",

                            page_data=camera_page,


                            # ==============================
                            # System
                            # ==============================

                            system=None,


                            # ==============================
                            # Theme
                            # ==============================

                            theme=theme,


                            # ==============================
                            # Viewport
                            # ==============================

                            viewport=viewport,


                            # ==============================
                            # Paths
                            # ==============================

                            template_dir=TEMPLATE_DIR,

                            output_root=OUTPUT_ROOT,


                            # ==============================
                            # Output Separation
                            #
                            # State must be included because
                            # otherwise all six state renders
                            # would use the same sample name.
                            # ==============================

                            output_subdir=(
                                f"shorts_camera/"
                                f"{theme_mode}/"
                                f"{camera_state}"
                            ),


                            # ==============================
                            # Scroll
                            # ==============================

                            scroll_percentages=(
                                SCROLL_PERCENTAGES
                            ),


                            # ==============================
                            # Full Page
                            # ==============================

                            save_full_page=(
                                SAVE_FULL_PAGE
                            ),


                            # ==============================
                            # Viewport
                            # ==============================

                            save_viewports=(
                                SAVE_VIEWPORTS
                            ),
                        )


        # ==================================================
        # Close Browser
        # ==================================================

        await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )