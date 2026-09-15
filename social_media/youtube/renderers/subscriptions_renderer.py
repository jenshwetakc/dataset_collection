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

from social_media.youtube.generators.subscriptions_generator import (
    generate_subscriptions_page,
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

# One synthetic page for responsive-layout testing.
# The same content is reused for every selected viewport.

NUM_SAMPLES = 50


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
        "YOUTUBE SUBSCRIPTIONS PAGE"
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
        # Samples
        # ==================================================

        for sample_index in tqdm(

            range(
                NUM_SAMPLES
            ),

            desc=
                "YouTube Subscriptions",
        ):

            # ==============================================
            # Generate Page Once
            #
            # The same:
            #
            # - channels
            # - videos
            # - thumbnails
            # - section structure
            # - theme
            #
            # is rendered on all four screen sizes.
            # ==============================================

            subscriptions_page = (
                generate_subscriptions_page()
            )


            # ==============================================
            # Generate Theme Once
            # ==============================================

            theme = (
                generate_accessible_theme()
            )


            # ==============================================
            # Debug Current Sample
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
                f"Subscribed channels: "
                f"{len(subscriptions_page['channels'])}"
            )


            print(
                f"Sections: "
                f"{len(subscriptions_page['sections'])}"
            )


            total_videos = sum(

                len(
                    section["videos"]
                )

                for section
                in subscriptions_page["sections"]
            )


            print(
                f"Total videos: "
                f"{total_videos}"
            )


            print(
                f"View mode: "
                f"{subscriptions_page['controls']['view_mode']}"
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
            # Render Same Page at Every Screen Size
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
                        "subscriptions",


                    # ======================================
                    # Template
                    # ======================================

                    template_name=
                        "pages/subscriptions.html",

                    context_key=
                        "page",

                    page_data=
                        subscriptions_page,


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
                        "subscriptions",


                    # ======================================
                    # Scroll Captures
                    # ======================================

                    scroll_percentages=
                        SCROLL_PERCENTAGES,


                    # ======================================
                    # Full Page Capture
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