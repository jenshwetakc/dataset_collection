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

from social_media.youtube.generators.home_generator import (
    generate_home_page,
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
# Config
# ==========================================================

NUM_SAMPLES = 50


# ----------------------------------------------------------
# Viewport mode:
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
# Scroll / Capture Config
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


    print(
        "\n=============================="
    )

    print(
        "YOUTUBE HOME DATASET"
    )

    print(
        "=============================="
    )


    print(
        f"Samples: {NUM_SAMPLES}"
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
            f"({viewport['width']}x"
            f"{viewport['height']}, "
            f"DPR={viewport.get('dpr', 1)})"
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
            desc="YouTube Home",
        ):

            # ==============================================
            # Generate Page Content
            #
            # Generate once so every viewport for this
            # sample uses the SAME content.
            # ==============================================

            home = (
                generate_home_page()
            )


            # ==============================================
            # Generate Accessible Theme
            #
            # No mode specified:
            # palette generator randomly chooses
            # light or dark.
            # ==============================================

            theme = (
                generate_accessible_theme()
            )


            # ==============================================
            # Render Viewports
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
                        "home",


                    # --------------------------------------
                    # Template
                    # --------------------------------------

                    template_name=
                        "pages/home.html",

                    context_key=
                        "page",

                    page_data=
                        home,


                    # --------------------------------------
                    # Optional system information
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
                        "home",


                    # --------------------------------------
                    # Capture Configuration
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