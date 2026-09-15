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

from social_media.youtube.generators.watch_generator import (
    generate_watch_page,
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

# ----------------------------------------------------------
# For UI testing:
#
# Generate ONE synthetic page and render that exact same
# page on each selected screen size.
#
# This allows us to visually compare responsive behavior.
# ----------------------------------------------------------

NUM_SAMPLES = 50


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORT_MODE = "selected"


# ----------------------------------------------------------
# Test each major screen category exactly once.
#
# Same synthetic content:
#
# mobile
# tablet
# laptop
# desktop
# ----------------------------------------------------------

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
    # Resolve Selected Viewports
    # ======================================================

    viewports = resolve_viewports(

        mode=
            VIEWPORT_MODE,

        selected=
            SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Configuration Debug
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE WATCH PAGE"
    )

    print(
        "=========================================="
    )


    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )


    print(
        f"Full page: "
        f"{SAVE_FULL_PAGE}"
    )


    print(
        f"Viewport screenshots: "
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
                "YouTube Watch",
        ):

            # ==============================================
            # Generate Watch Page
            #
            # IMPORTANT:
            #
            # Generate ONCE here.
            #
            # Do NOT generate separately inside the
            # viewport loop.
            #
            # This guarantees that mobile/tablet/laptop/
            # desktop all show exactly the same content.
            # ==============================================

            watch_page = (
                generate_watch_page()
            )


            # ==============================================
            # Generate Theme Once
            #
            # Same theme for every viewport belonging
            # to this sample.
            # ==============================================

            theme = (
                generate_accessible_theme()
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
                f"Title: "
                f"{watch_page['video']['title']}"
            )


            print(
                f"Channel: "
                f"{watch_page['video']['channel']['name']}"
            )


            print(
                f"Comments generated: "
                f"{len(watch_page['comments']['items'])}"
            )


            print(
                f"Recommendations generated: "
                f"{len(watch_page['recommendations'])}"
            )


            print(
                f"Theme: "
                f"{theme.get('mode')}"
            )


            print(
                f"WCAG pass: "
                f"{theme.get('wcag_pass')}"
            )


            # ==============================================
            # Render Same Page on Every Screen
            # ==============================================

            for viewport in viewports:

                print(

                    "\nRendering: "

                    f"{viewport['name']} "

                    f"("
                    f"{viewport['width']}"
                    f"x"
                    f"{viewport['height']}"
                    f")"
                )


                await render_page(

                    # ======================================
                    # Browser
                    # ======================================

                    browser=
                        browser,


                    # ======================================
                    # Sample
                    # ======================================

                    sample_index=
                        sample_index,

                    page_type=
                        "watch",


                    # ======================================
                    # Template
                    # ======================================

                    template_name=
                        "pages/watch.html",

                    context_key=
                        "page",

                    page_data=
                        watch_page,


                    # ======================================
                    # System Data
                    # ======================================

                    system=
                        None,


                    # ======================================
                    # Theme
                    # ======================================

                    theme=
                        theme,


                    # ======================================
                    # Current Viewport
                    # ======================================

                    viewport=
                        viewport,


                    # ======================================
                    # Paths
                    # ======================================

                    template_dir=
                        TEMPLATE_DIR,

                    output_root=
                        OUTPUT_ROOT,

                    output_subdir=
                        "watch",


                    # ======================================
                    # Scroll Capture
                    # ======================================

                    scroll_percentages=
                        SCROLL_PERCENTAGES,


                    # ======================================
                    # Full Page
                    # ======================================

                    save_full_page=
                        SAVE_FULL_PAGE,


                    # ======================================
                    # Viewport Captures
                    # ======================================

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