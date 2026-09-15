from __future__ import annotations

import asyncio

from pathlib import Path

from playwright.async_api import (
    async_playwright,
)

from tqdm import tqdm


from social_media.youtube.renderers.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.youtube.generators.fullscreen_player_generator import (
    PLAYER_STATES,
    generate_fullscreen_player_page,
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
# Player States
# ==========================================================

# We explicitly render every important player state.

PLAYER_STATES_TO_RENDER = [
    "controls_visible",
    "controls_hidden",
    "paused",
    "seeking_backward",
    "seeking_forward",
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


# Fullscreen player needs landscape coverage in addition
# to our normal desktop/tablet/mobile validation.

SELECTED_VIEWPORTS = [
    "standard_iphone",
    "tablet_landscape",
    "laptop",
    "desktop_fhd",
]

# ==========================================================
# Scroll Configuration
# ==========================================================

# Fullscreen player has no page scrolling.
#
# We only capture the viewport at scroll position 0.

SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Capture Configuration
# ==========================================================

# A "full page" screenshot is not useful here because
# the document itself is exactly one fullscreen viewport.

SAVE_FULL_PAGE = False

SAVE_VIEWPORTS = True


# ==========================================================
# Validation
# ==========================================================

def validate_player_states() -> None:

    unknown_states = [

        state

        for state
        in PLAYER_STATES_TO_RENDER

        if state
        not in PLAYER_STATES
    ]


    if unknown_states:

        raise ValueError(
            "Unknown player states: "
            f"{unknown_states}. "
            f"Available states: {PLAYER_STATES}"
        )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validate Configuration
    # ======================================================

    validate_player_states()


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
        "YOUTUBE FULLSCREEN PLAYER"
    )

    print(
        "=========================================="
    )


    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )


    print(
        f"Player states: "
        f"{PLAYER_STATES_TO_RENDER}"
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

            if viewport["width"]
            > viewport["height"]

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

        browser = (
            await p.chromium.launch(
                headless=True
            )
        )


        # ==================================================
        # Samples
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Fullscreen Player",
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
            # Player States
            # ==============================================

            for player_state in PLAYER_STATES_TO_RENDER:

                # ==========================================
                # Generate This State ONCE
                #
                # Important:
                #
                # Light and dark mode use the exact same:
                #
                # - video frame
                # - title
                # - channel
                # - playback position
                # - volume
                # - captions state
                # - player controls
                #
                # Only the theme context changes.
                # ==========================================

                player_page = (
                    generate_fullscreen_player_page(
                        state=player_state
                    )
                )


                video = (
                    player_page["video"]
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    f"Player state: "
                    f"{player_state}"
                )


                print(
                    f"Video: "
                    f"{video['title']}"
                )


                print(
                    f"Playback: "
                    f"{video['current_time_text']}"
                    f" / "
                    f"{video['duration_text']}"
                )


                print(
                    f"Progress: "
                    f"{video['progress_percent']}%"
                )


                print(
                    f"Paused: "
                    f"{player_page['playback']['paused']}"
                )


                print(
                    f"Controls visible: "
                    f"{player_page['playback']['controls_visible']}"
                )


                if player_page["seek_feedback"]:

                    print(
                        f"Seek feedback: "
                        f"{player_page['seek_feedback']['direction']}"
                        f" "
                        f"{player_page['seek_feedback']['seconds']}s"
                    )


                # ==========================================
                # Theme
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
                    # Viewports
                    # ======================================

                    for viewport in viewports:

                        print(
                            "Rendering: "
                            f"{player_state}"
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

                            browser=
                                browser,


                            # ==============================
                            # Sample
                            # ==============================

                            sample_index=
                                sample_index,

                            page_type=
                                "fullscreen_player",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=
                                "pages/fullscreen_player.html",

                            context_key=
                                "page",

                            page_data=
                                player_page,


                            # ==============================
                            # System
                            # ==============================

                            system=
                                None,


                            # ==============================
                            # Theme
                            # ==============================

                            theme=
                                theme,


                            # ==============================
                            # Viewport
                            # ==============================

                            viewport=
                                viewport,


                            # ==============================
                            # Paths
                            # ==============================

                            template_dir=
                                TEMPLATE_DIR,

                            output_root=
                                OUTPUT_ROOT,


                            # ==============================
                            # IMPORTANT
                            #
                            # State must be part of output
                            # directory; otherwise different
                            # states would overwrite each
                            # other because page_type and
                            # sample_index are identical.
                            # ==============================

                            output_subdir=(
                                f"fullscreen_player/"
                                f"{theme_mode}/"
                                f"{player_state}"
                            ),


                            # ==============================
                            # No Scrolling
                            # ==============================

                            scroll_percentages=
                                SCROLL_PERCENTAGES,


                            # ==============================
                            # Full Page
                            # ==============================

                            save_full_page=
                                SAVE_FULL_PAGE,


                            # ==============================
                            # Viewport
                            # ==============================

                            save_viewports=
                                SAVE_VIEWPORTS,
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