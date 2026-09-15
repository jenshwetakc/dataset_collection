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

from social_media.youtube.generators.tv_home_generator import (
    TV_HOME_STATES,
    generate_tv_home_page,
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
# TV States
# ==========================================================

TV_STATES_TO_RENDER = [
    "home",
    "navigation_focused",
    "video_focused",
    "profile_menu",
    "search_focused",
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

# TV UI is intentionally targeted at large displays rather
# than mobile/tablet layouts.

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

# This is treated as a fixed living-room screen.
# We capture the visible TV viewport rather than scrolling
# through the document.

SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = False

SAVE_VIEWPORTS = True


# ==========================================================
# Validation
# ==========================================================

def validate_tv_states() -> None:

    unknown_states = [
        state
        for state in TV_STATES_TO_RENDER
        if state not in TV_HOME_STATES
    ]

    if unknown_states:

        raise ValueError(
            "Unknown TV home states: "
            f"{unknown_states}. "
            f"Available states: "
            f"{TV_HOME_STATES}"
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
        f"Hero visible: "
        f"{page['layout']['show_hero']}"
    )

    print(
        f"Rows visible: "
        f"{page['layout']['show_rows']}"
    )

    print(
        f"Profile menu: "
        f"{page['profile_menu']['open']}"
    )

    print(
        f"Search overlay: "
        f"{page['layout']['show_search_overlay']}"
    )

    print(
        f"Rows: "
        f"{len(page['rows'])}"
    )

    print(
        "Navigation:"
    )

    for item in page["navigation"]:

        print(
            f"  - "
            f"{item['label']}"
            f" | "
            f"selected={item['selected']}"
            f" | "
            f"focused={item['focused']}"
        )

    print(
        "Content rows:"
    )

    for row in page["rows"]:

        focused_items = [
            video["title"]
            for video in row["items"]
            if video["focused"]
        ]

        print(
            f"  - "
            f"{row['title']}"
            f" | "
            f"items={len(row['items'])}"
            f" | "
            f"focused={focused_items}"
        )

    print(
        f"Profiles: "
        f"{len(page['profiles'])}"
    )

    print(
        f"Search query: "
        f"{page['search']['query']!r}"
    )

    print(
        f"Search suggestions: "
        f"{len(page['search']['suggestions'])}"
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validate Configuration
    # ======================================================

    validate_tv_states()


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
        "YOUTUBE TV HOME"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )

    print(
        f"TV states: "
        f"{TV_STATES_TO_RENDER}"
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
        "\nTesting TV viewports:"
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

        browser = await p.chromium.launch(
            headless=True
        )


        # ==================================================
        # Sample Loop
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube TV Home",
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

            for tv_state in TV_STATES_TO_RENDER:

                # ==========================================
                # Generate this TV state ONCE.
                #
                # We deliberately reuse the exact same page
                # data across:
                #
                # - light/dark
                # - 1080p
                # - 1440p
                # - 4K
                #
                # That keeps visual comparisons controlled.
                # ==========================================

                tv_page = (
                    generate_tv_home_page(
                        state=tv_state
                    )
                )


                print(
                    "\n"
                    "======================================"
                )

                print_page_debug(
                    tv_page
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
                            f"{tv_state}"
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

                            page_type="tv_home",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=(
                                "pages/tv_home.html"
                            ),

                            context_key="page",

                            page_data=tv_page,


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
                            # ==============================

                            output_subdir=(
                                f"tv_home/"
                                f"{theme_mode}/"
                                f"{tv_state}"
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