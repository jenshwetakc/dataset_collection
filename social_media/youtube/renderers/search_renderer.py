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

from social_media.youtube.generators.search_generator import (
    generate_search_page,
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


# ----------------------------------------------------------
# Viewport mode options:
#
# "all"
# "mobile"
# "tablet"
# "laptop"
# "desktop"
# "selected"
# "random"
# ----------------------------------------------------------

VIEWPORT_MODE = "selected"


SELECTED_VIEWPORTS = [
    "standard_iphone",
    "tablet_landscape",
    "laptop",
    "desktop_fhd",
]


# ==========================================================
# Scroll / Capture Configuration
# ==========================================================

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]


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
    # Debug Information
    # ======================================================

    print(
        "\n=============================="
    )

    print(
        "YOUTUBE SEARCH DATASET"
    )

    print(
        "=============================="
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
        "\nViewports:"
    )


    for viewport in viewports:

        print(

            f"  - "
            f"{viewport['name']} "

            f"("
            f"{viewport['width']}x"
            f"{viewport['height']}, "

            f"DPR="
            f"{viewport.get('dpr', 1)}"
            f")"
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
            range(NUM_SAMPLES),
            desc="YouTube Search",
        ):

            # ==============================================
            # Generate Search Page
            #
            # Generate exactly ONCE per sample.
            #
            # Every viewport and scroll position for this
            # sample will therefore use the same:
            #
            # - search query
            # - search results
            # - channels
            # - thumbnails
            # - text
            # - theme
            # ==============================================

            search_page = (
                generate_search_page()
            )


            # ==============================================
            # Accessible Theme
            #
            # mode=None means our palette generator can
            # randomly choose light or dark.
            # ==============================================

            theme = (
                generate_accessible_theme()
            )


            # ==============================================
            # Debug Current Sample
            # ==============================================

            print(
                "\n------------------------------"
            )

            print(
                f"Sample: "
                f"{sample_index}"
            )

            print(
                f"Query: "
                f"{search_page['query']}"
            )

            print(
                f"Results: "
                f"{len(search_page['results'])}"
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
                f"WCAG: "
                f"{theme.get('wcag_pass')}"
            )


            # ==============================================
            # Render Every Selected Viewport
            # ==============================================

            for viewport in viewports:

                await render_page(

                    # --------------------------------------
                    # Browser
                    # --------------------------------------

                    browser=
                        browser,


                    # --------------------------------------
                    # Sample
                    # --------------------------------------

                    sample_index=
                        sample_index,

                    page_type=
                        "search",


                    # --------------------------------------
                    # Template
                    # --------------------------------------

                    template_name=
                        "pages/search.html",

                    context_key=
                        "page",

                    page_data=
                        search_page,


                    # --------------------------------------
                    # System information
                    #
                    # Search currently has no separate
                    # synthetic mobile system bar.
                    # --------------------------------------

                    system=
                        None,


                    # --------------------------------------
                    # Theme
                    # --------------------------------------

                    theme=
                        theme,


                    # --------------------------------------
                    # Viewport
                    # --------------------------------------

                    viewport=
                        viewport,


                    # --------------------------------------
                    # Paths
                    # --------------------------------------

                    template_dir=
                        TEMPLATE_DIR,

                    output_root=
                        OUTPUT_ROOT,

                    output_subdir=
                        "search",


                    # --------------------------------------
                    # Full Page + Scroll Capture
                    # --------------------------------------

                    scroll_percentages=
                        SCROLL_PERCENTAGES,

                    save_full_page=
                        SAVE_FULL_PAGE,

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