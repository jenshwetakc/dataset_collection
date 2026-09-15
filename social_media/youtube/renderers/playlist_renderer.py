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

from social_media.youtube.generators.playlist_generator import (
    generate_playlist_page,
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
        "YOUTUBE PLAYLIST PAGE"
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
            desc="YouTube Playlist",
        ):

            # ==============================================
            # Generate Playlist Page Once
            #
            # Important:
            # The exact same playlist content is reused for:
            #
            # - light mode
            # - dark mode
            # - mobile
            # - tablet
            # - laptop
            # - desktop
            #
            # Only responsive layout and theme change.
            # ==============================================

            playlist_page = (
                generate_playlist_page()
            )


            playlist = (
                playlist_page["playlist"]
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
                f"Playlist: "
                f"{playlist['title']}"
            )


            print(
                f"Owner: "
                f"{playlist['owner']['name']}"
            )


            print(
                f"Visibility: "
                f"{playlist['visibility']}"
            )


            print(
                f"Videos: "
                f"{playlist['video_count']}"
            )


            print(
                f"Views: "
                f"{playlist['total_views_text']}"
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
                            "playlist",


                        # ==================================
                        # Template
                        # ==================================

                        template_name=
                            "pages/playlist.html",

                        context_key=
                            "page",

                        page_data=
                            playlist_page,


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
                        # Separate Light / Dark
                        # ==================================

                        output_subdir=(
                            f"playlist/"
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