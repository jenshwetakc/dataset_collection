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

from social_media.youtube.generators.live_chat_generator import (
    LIVE_CHAT_STATES,
    generate_live_chat_page,
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
# Live Chat States
# ==========================================================

LIVE_CHAT_STATES_TO_RENDER = [
    "normal",
    "pinned_message",
    "super_chat",
    "members_only",
    "chat_paused",
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

# The outer page is mostly a compact watch/live layout.
# The chat itself scrolls internally, so repeated outer-page
# scroll captures do not add much value here.

SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = True

SAVE_VIEWPORTS = True
import inspect
print(
    "RENDER_PAGE SIGNATURE:",
    inspect.signature(
        render_page
    ),
)

# ==========================================================
# Validate States
# ==========================================================

def validate_live_chat_states() -> None:

    unknown_states = [
        state
        for state in LIVE_CHAT_STATES_TO_RENDER
        if state not in LIVE_CHAT_STATES
    ]

    if unknown_states:

        raise ValueError(
            "Unknown live chat states: "
            f"{unknown_states}. "
            f"Available states: "
            f"{LIVE_CHAT_STATES}"
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
        f"Title: "
        f"{page['livestream']['title']}"
    )

    print(
        f"Channel: "
        f"{page['livestream']['channel']['name']}"
    )

    print(
        f"Viewers: "
        f"{page['livestream']['viewer_count_text']}"
    )

    print(
        f"Messages: "
        f"{len(page['chat_messages'])}"
    )

    print(
        f"Pinned message: "
        f"{page['pinned_message'].get('enabled', False)}"
    )

    print(
        f"Chat paused: "
        f"{page['chat_header']['paused']}"
    )

    print(
        f"Members only: "
        f"{page['chat_input']['members_only']}"
    )

    print(
        f"Chat input enabled: "
        f"{page['chat_input']['enabled']}"
    )

    super_chat_count = sum(
        1
        for message in page["chat_messages"]
        if message["type"] == "super_chat"
    )

    print(
        f"Super chats: "
        f"{super_chat_count}"
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validate Configuration
    # ======================================================

    validate_live_chat_states()


    # ======================================================
    # Resolve Viewports
    # ======================================================

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Configuration Debug
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE LIVE CHAT"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )

    print(
        f"States: "
        f"{LIVE_CHAT_STATES_TO_RENDER}"
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
        # Sample Loop
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Live Chat",
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

            for live_chat_state in (
                LIVE_CHAT_STATES_TO_RENDER
            ):

                # ==========================================
                # Generate This State ONCE
                #
                # Important:
                # the exact same livestream/chat data is
                # reused across every theme and viewport.
                # ==========================================

                live_chat_page = (
                    generate_live_chat_page(
                        state=live_chat_state
                    )
                )


                print(
                    "\n"
                    "======================================"
                )

                print_page_debug(
                    live_chat_page
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
                            f"{live_chat_state}"
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
                                "live_chat",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=
                                "pages/live_chat.html",

                            context_key=
                                "page",

                            page_data=
                                live_chat_page,


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
                            # Output Separation
                            #
                            # Every state needs its own
                            # directory to avoid overwriting
                            # the same sample index.
                            # ==============================

                            output_subdir=(
                                f"live_chat/"
                                f"{theme_mode}/"
                                f"{live_chat_state}"
                            ),


                            # ==============================
                            # Outer Page Scroll
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