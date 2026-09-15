import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.chat_generator import (
    generate_chat_page,
    generate_system_status,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORT_MODE = "selected"


# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "tablet_landscape",
#     "laptop",
#     "desktop_fhd",
# ]
SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_android",
    "standard_iphone",
    "large_mobile",
    "mobile_landscape",
    "tablet_portrait",
    "large_tablet_portrait",
    "tablet_landscape",
    "foldable",
    "small_laptop",
    "laptop",
    "large_laptop",
    "desktop_fhd",
    "desktop_qhd",
    "desktop_4k",
    "ultrawide",
]

# ==========================================================
# Main
# ==========================================================

async def main():

    # ------------------------------------------------------
    # Resolve Viewports
    # ------------------------------------------------------

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    print(
        "\nRendering Chats page"
    )

    print(
        "Viewports:"
    )


    for viewport in viewports:

        print(
            f"  {viewport['name']} | "
            f"{viewport['category']} | "
            f"{viewport.get('orientation', 'unknown')} | "
            f"{viewport.get('size_class', 'unknown')} | "
            f"{viewport['width']}x"
            f"{viewport['height']} | "
            f"DPR={viewport.get('dpr', 1)}"
        )


    # ------------------------------------------------------
    # Start Playwright
    # ------------------------------------------------------

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )


        # ==================================================
        # Generate Samples
        # ==================================================

        for sample_index in range(
            1,
            NUM_SAMPLES + 1,
        ):

            print(
                f"\nGenerating sample "
                f"{sample_index}/{NUM_SAMPLES}"
            )


            # ----------------------------------------------
            # Generate ONE Chats state
            #
            # The same generated state is used across
            # every selected viewport.
            # ----------------------------------------------

            page_data = (
                generate_chat_page()
            )


            # ----------------------------------------------
            # System Status
            # ----------------------------------------------

            system = (
                generate_system_status()
            )


            # ----------------------------------------------
            # Theme
            # ----------------------------------------------

            theme_mode = random.choice(
                [
                    "light",
                    "dark",
                ]
            )


            theme = (
                generate_accessible_theme(
                    mode=theme_mode
                )
            )


            # ----------------------------------------------
            # Debug
            # ----------------------------------------------

            print(
                "Theme:",
                theme_mode
            )


            if "selected_filter" in page_data:

                print(
                    "Selected filter:",
                    page_data[
                        "selected_filter"
                    ]
                )


            if "chats" in page_data:

                print(
                    "Chat count:",
                    len(
                        page_data[
                            "chats"
                        ]
                    )
                )


            # ----------------------------------------------
            # Render SAME page across all viewports
            # ----------------------------------------------

            for viewport in viewports:

                print(
                    f"  Rendering "
                    f"{viewport['name']}"
                )


                await render_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "chats",

                    template_name=
                        "chats.html",

                    context_key=
                        "page",

                    page_data=
                        page_data,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "chats",
                )


        # ==================================================
        # Close Browser
        # ==================================================

        await browser.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )