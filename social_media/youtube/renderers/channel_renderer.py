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

from social_media.youtube.generators.channel_generator import (
    generate_channel_page,
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
# Main
# ==========================================================

async def main():

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
        "YOUTUBE CHANNEL PAGE"
    )

    print(
        "=========================================="
    )


    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )


    print(
        f"Themes: "
        f"{THEME_MODES}"
    )


    print(
        f"Full page capture: "
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

        print(
            f"  - "
            f"{viewport['name']}"
            f" | "
            f"{viewport['width']}"
            f"x"
            f"{viewport['height']}"
            f" | DPR="
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
        # Samples
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Channel",
        ):

            # ==============================================
            # Generate Channel Page ONCE
            #
            # The exact same channel data is used for:
            #
            # light
            # dark
            # mobile
            # tablet
            # laptop
            # desktop
            #
            # This gives us a clean comparison of theme and
            # responsive layout.
            # ==============================================

            channel_page = (
                generate_channel_page()
            )


            channel = (
                channel_page["channel"]
            )


            # ==============================================
            # Sample Debug
            # ==============================================

            print(
                "\n"
                "------------------------------------------"
            )


            print(
                f"Sample: "
                f"{sample_index}"
            )


            print(
                f"Channel: "
                f"{channel['name']}"
            )


            print(
                f"Handle: "
                f"{channel['handle']}"
            )


            print(
                f"Subscribers: "
                f"{channel['subscribers_text']}"
            )


            print(
                f"Videos: "
                f"{len(channel_page['videos'])}"
            )


            print(
                f"Shorts: "
                f"{len(channel_page['shorts'])}"
            )


            print(
                f"Playlists: "
                f"{len(channel_page['playlists'])}"
            )


            print(
                f"Subscribed: "
                f"{channel['subscribed']}"
            )


            # ==============================================
            # Light + Dark
            # ==============================================

            for theme_mode in THEME_MODES:

                # ==========================================
                # Generate Explicit Theme
                # ==========================================

                theme = (
                    generate_accessible_theme(
                        mode=theme_mode
                    )
                )


                print(
                    "\n"
                    "======================================"
                )


                print(
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


                # ==========================================
                # Render Every Viewport
                # ==========================================

                for viewport in viewports:

                    print(
                        "\nRendering: "
                        f"{theme_mode} | "
                        f"{viewport['name']} "
                        f"("
                        f"{viewport['width']}"
                        f"x"
                        f"{viewport['height']}"
                        f")"
                    )


                    await render_page(

                        # ==================================
                        # Browser
                        # ==================================

                        browser=
                            browser,


                        # ==================================
                        # Sample
                        # ==================================

                        sample_index=
                            sample_index,

                        page_type=
                            "channel",


                        # ==================================
                        # Template
                        # ==================================

                        template_name=
                            "pages/channel.html",

                        context_key=
                            "page",

                        page_data=
                            channel_page,


                        # ==================================
                        # System
                        # ==================================

                        system=
                            None,


                        # ==================================
                        # Theme
                        # ==================================

                        theme=
                            theme,


                        # ==================================
                        # Viewport
                        # ==================================

                        viewport=
                            viewport,


                        # ==================================
                        # Paths
                        # ==================================

                        template_dir=
                            TEMPLATE_DIR,

                        output_root=
                            OUTPUT_ROOT,


                        # ==================================
                        # Keep light/dark separate
                        # ==================================

                        output_subdir=(
                            f"channel/"
                            f"{theme_mode}"
                        ),


                        # ==================================
                        # Scroll Captures
                        # ==================================

                        scroll_percentages=
                            SCROLL_PERCENTAGES,


                        # ==================================
                        # Full Page Capture
                        # ==================================

                        save_full_page=
                            SAVE_FULL_PAGE,


                        # ==================================
                        # Viewport Captures
                        # ==================================

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