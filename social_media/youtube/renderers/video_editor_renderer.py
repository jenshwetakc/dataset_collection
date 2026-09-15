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

from social_media.youtube.generators.video_editor_generator import (
    EDITOR_STATES,
    generate_video_editor_page,
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
# Editor States
# ==========================================================

EDITOR_STATES_TO_RENDER = [
    "idle",
    "playing",
    "trim_start_selected",
    "trim_end_selected",
    "playhead_middle",
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

# The editor is intended to fit inside the viewport.
# We only need the initial screen position.

SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = False

SAVE_VIEWPORTS = True


# ==========================================================
# Validate Editor States
# ==========================================================

def validate_editor_states() -> None:

    unknown_states = [
        state
        for state in EDITOR_STATES_TO_RENDER
        if state not in EDITOR_STATES
    ]

    if unknown_states:

        raise ValueError(
            "Unknown editor states: "
            f"{unknown_states}. "
            f"Available states: {EDITOR_STATES}"
        )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validation
    # ======================================================

    validate_editor_states()


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
        "YOUTUBE VIDEO EDITOR"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: {NUM_SAMPLES}"
    )

    print(
        f"Editor states: {EDITOR_STATES_TO_RENDER}"
    )

    print(
        f"Themes: {THEME_MODES}"
    )

    print(
        f"Save full page: {SAVE_FULL_PAGE}"
    )

    print(
        f"Save viewport: {SAVE_VIEWPORTS}"
    )

    print(
        f"Scroll positions: {SCROLL_PERCENTAGES}"
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
            f"{viewport['width']}x{viewport['height']}"
            f" | "
            f"{orientation}"
            f" | "
            f"DPR={viewport.get('dpr', 1)}"
        )


    # ======================================================
    # Playwright
    # ======================================================

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )


        # ==================================================
        # Samples
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Video Editor",
        ):

            print(
                "\n"
                "------------------------------------------"
            )

            print(
                f"Sample: {sample_index}"
            )


            # ==============================================
            # Editor States
            # ==============================================

            for editor_state in EDITOR_STATES_TO_RENDER:

                # ==========================================
                # Generate state ONCE
                #
                # Important:
                # this same generated editor data is reused
                # for all themes and all viewports.
                # ==========================================

                editor_page = (
                    generate_video_editor_page(
                        state=editor_state
                    )
                )


                # ==========================================
                # Debug State
                # ==========================================

                print(
                    "\n"
                    "======================================"
                )

                print(
                    f"Editor state: {editor_state}"
                )

                print(
                    f"Video: "
                    f"{editor_page['video']['title']}"
                )

                print(
                    f"Duration: "
                    f"{editor_page['video']['duration_text']}"
                )

                print(
                    f"Trim: "
                    f"{editor_page['trim']['start_text']}"
                    f" -> "
                    f"{editor_page['trim']['end_text']}"
                )

                print(
                    f"Selected duration: "
                    f"{editor_page['trim']['selected_duration_text']}"
                )

                print(
                    f"Playhead: "
                    f"{editor_page['playhead']['current_time_text']}"
                )

                print(
                    f"Playing: "
                    f"{editor_page['playback']['playing']}"
                )

                print(
                    f"Start selected: "
                    f"{editor_page['handles']['start_selected']}"
                )

                print(
                    f"End selected: "
                    f"{editor_page['handles']['end_selected']}"
                )


                # ==========================================
                # Theme Loop
                # ==========================================

                for theme_mode in THEME_MODES:

                    theme = generate_accessible_theme(
                        mode=theme_mode
                    )


                    print(
                        "\n"
                        f"Theme: {theme_mode}"
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
                            f"{editor_state}"
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

                            page_type="video_editor",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=(
                                "pages/video_editor.html"
                            ),

                            context_key="page",

                            page_data=editor_page,


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
                            # Output Structure
                            #
                            # Keep each editor state separate
                            # so files cannot overwrite.
                            # ==============================

                            output_subdir=(
                                f"video_editor/"
                                f"{theme_mode}/"
                                f"{editor_state}"
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