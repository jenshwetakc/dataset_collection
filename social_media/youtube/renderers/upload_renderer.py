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

from social_media.youtube.generators.upload_generator import (
    UPLOAD_STATES,
    generate_upload_video_page,
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
# Upload States
# ==========================================================

UPLOAD_STATES_TO_RENDER = [
    "select_file",
    "uploading",
    "details",
    "processing",
    "ready_to_publish",
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

# Unlike fullscreen/editor pages, the details portion of
# the upload UI can become taller than the viewport.
#
# Therefore we keep scroll captures for this UI.

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = True

SAVE_VIEWPORTS = True


# ==========================================================
# Validate Upload States
# ==========================================================

def validate_upload_states() -> None:

    unknown_states = [
        state
        for state in UPLOAD_STATES_TO_RENDER
        if state not in UPLOAD_STATES
    ]

    if unknown_states:

        raise ValueError(
            "Unknown upload states: "
            f"{unknown_states}. "
            f"Available states: {UPLOAD_STATES}"
        )


# ==========================================================
# Debug
# ==========================================================

def print_page_debug(
    page: dict,
) -> None:

    print(
        f"File: "
        f"{page['file']['filename']}"
    )

    print(
        f"Size: "
        f"{page['file']['size_text']}"
    )

    print(
        f"Duration: "
        f"{page['file']['duration_text']}"
    )

    print(
        f"Resolution: "
        f"{page['file']['resolution']}"
    )

    print(
        f"Upload status: "
        f"{page['progress']['status']}"
    )

    print(
        f"Upload percent: "
        f"{page['progress']['percent']}%"
    )

    print(
        f"Visibility: "
        f"{page['visibility']['selected']}"
    )

    print(
        f"Made for kids: "
        f"{page['audience']['made_for_kids']}"
    )

    print(
        "Layout:"
    )

    for key, value in page["layout"].items():

        print(
            f"  {key}: "
            f"{value}"
        )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validation
    # ======================================================

    validate_upload_states()


    # ======================================================
    # Resolve Viewports
    # ======================================================

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Configuration
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE UPLOAD VIDEO"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )

    print(
        f"Upload states: "
        f"{UPLOAD_STATES_TO_RENDER}"
    )

    print(
        f"Themes: "
        f"{THEME_MODES}"
    )

    print(
        f"Full-page capture: "
        f"{SAVE_FULL_PAGE}"
    )

    print(
        f"Viewport capture: "
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
        # Sample Loop
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Upload",
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

            for upload_state in UPLOAD_STATES_TO_RENDER:

                # ==========================================
                # Generate state ONCE
                #
                # This exact same page data is reused for:
                #
                # - light
                # - dark
                # - mobile
                # - tablet
                # - laptop
                # - desktop
                #
                # Therefore comparisons are controlled.
                # ==========================================

                upload_page = (
                    generate_upload_video_page(
                        state=upload_state
                    )
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    f"Upload state: "
                    f"{upload_state}"
                )

                print_page_debug(
                    upload_page
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
                            f"{upload_state}"
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

                            page_type="upload",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=(
                                "pages/upload.html"
                            ),

                            context_key="page",

                            page_data=upload_page,


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
                            # State + Theme Separation
                            #
                            # This prevents:
                            #
                            # select_file sample 0
                            # uploading sample 0
                            #
                            # from overwriting each other.
                            # ==============================

                            output_subdir=(
                                f"upload/"
                                f"{theme_mode}/"
                                f"{upload_state}"
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
                            # Viewports
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