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

from social_media.youtube.generators.shorts_generator import (
    generate_shorts_page,
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

# One generated Shorts page.
#
# We render the exact same page on each target viewport
# so we can inspect responsive behavior consistently.

NUM_SAMPLES = 50


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORT_MODE = "selected"


# ----------------------------------------------------------
# Check each major screen size once
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
    # Resolve Viewports
    # ======================================================

    viewports = resolve_viewports(

        mode=
            VIEWPORT_MODE,

        selected=
            SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Debug Configuration
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE SHORTS PAGE"
    )

    print(
        "=========================================="
    )


    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
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
        # Generate Samples
        # ==================================================

        for sample_index in tqdm(

            range(
                NUM_SAMPLES
            ),

            desc=
                "YouTube Shorts",
        ):

            # ==============================================
            # Generate Shorts Page ONCE
            #
            # Important:
            # Do not generate inside the viewport loop.
            #
            # All four viewport screenshots should contain
            # exactly the same:
            #
            # - shorts
            # - images
            # - creators
            # - captions
            # - counts
            # - theme
            # ==============================================

            shorts_page = (
                generate_shorts_page()
            )


            # ==============================================
            # Theme
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
                f"Shorts generated: "
                f"{len(shorts_page['shorts'])}"
            )


            print(
                f"Theme: "
                f"{theme.get('mode')}"
            )


            print(
                f"Seed: "
                f"{theme.get('seed')}"
            )


            print(
                f"WCAG pass: "
                f"{theme.get('wcag_pass')}"
            )


            # ==============================================
            # Optional Debug for First Short
            # ==============================================

            if shorts_page["shorts"]:

                first_short = (
                    shorts_page["shorts"][0]
                )


                print(
                    f"First channel: "
                    f"{first_short['channel']['name']}"
                )


                print(
                    f"First caption: "
                    f"{first_short['caption']}"
                )


                print(
                    f"First image exists: "
                    f"{bool(first_short['image'])}"
                )


            # ==============================================
            # Render Same Page Across All Screens
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
                        "shorts",


                    # ======================================
                    # Template
                    # ======================================

                    template_name=
                        "pages/shorts.html",

                    context_key=
                        "page",

                    page_data=
                        shorts_page,


                    # ======================================
                    # System
                    # ======================================

                    system=
                        None,


                    # ======================================
                    # Theme
                    # ======================================

                    theme=
                        theme,


                    # ======================================
                    # Viewport
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
                        "shorts",


                    # ======================================
                    # Scroll Positions
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