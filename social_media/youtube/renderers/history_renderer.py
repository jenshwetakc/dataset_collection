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

from social_media.youtube.generators.history_generator import (
    generate_history_page,
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
        "YOUTUBE HISTORY PAGE"
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

            range(
                NUM_SAMPLES
            ),

            desc=
                "YouTube History",
        ):

            # ==============================================
            # Generate History Page Once
            #
            # The exact same content is reused for:
            #
            # - light
            # - dark
            # - mobile
            # - tablet
            # - laptop
            # - desktop
            #
            # This lets us compare only visual/theme/layout
            # differences.
            # ==============================================

            history_page = (
                generate_history_page()
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
                f"Sections: "
                f"{len(history_page['sections'])}"
            )


            total_videos = sum(

                len(
                    section["videos"]
                )

                for section
                in history_page["sections"]
            )


            print(
                f"Total history videos: "
                f"{total_videos}"
            )


            print(
                f"History paused: "
                f"{history_page['controls']['history_paused']}"
            )


            # ==============================================
            # Light + Dark
            # ==============================================

            for theme_mode in THEME_MODES:

                # ==========================================
                # Explicit Theme
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
                            "history",


                        # ==================================
                        # Template
                        # ==================================

                        template_name=
                            "pages/history.html",

                        context_key=
                            "page",

                        page_data=
                            history_page,


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
                        # Separate light / dark output
                        # ==================================

                        output_subdir=(
                            f"history/"
                            f"{theme_mode}"
                        ),


                        # ==================================
                        # Scroll Capture
                        # ==================================

                        scroll_percentages=
                            SCROLL_PERCENTAGES,


                        # ==================================
                        # Full Page Capture
                        # ==================================

                        save_full_page=
                            SAVE_FULL_PAGE,


                        # ==================================
                        # Viewport Capture
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