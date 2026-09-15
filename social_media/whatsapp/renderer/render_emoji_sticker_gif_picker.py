import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.emoji_sticker_gif_generator import (
    generate_emoji_sticker_gif_page,
)

from social_media.whatsapp.generators.chat_generator import (
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


SELECTED_VIEWPORTS = [
    "standard_iphone",
    "tablet_landscape",
    "laptop",
    "desktop_fhd",
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
        "\nRendering Emoji / Sticker / GIF Picker"
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
            # Generate ONE picker state
            #
            # Same picker state is reused across every
            # selected viewport.
            # ----------------------------------------------

            picker = (
                generate_emoji_sticker_gif_page()
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

            if isinstance(
                picker,
                dict,
            ):

                if "active_tab" in picker:

                    print(
                        "Active tab:",
                        picker[
                            "active_tab"
                        ]
                    )


                if "emoji_count" in picker:

                    print(
                        "Emoji count:",
                        picker[
                            "emoji_count"
                        ]
                    )


                if "sticker_count" in picker:

                    print(
                        "Sticker count:",
                        picker[
                            "sticker_count"
                        ]
                    )


                if "gif_count" in picker:

                    print(
                        "GIF count:",
                        picker[
                            "gif_count"
                        ]
                    )


                if "selected_category" in picker:

                    print(
                        "Selected category:",
                        picker[
                            "selected_category"
                        ]
                    )


                search = picker.get(
                    "search",
                    {}
                )


                if isinstance(
                    search,
                    dict,
                ):

                    print(
                        "Search active:",
                        search.get(
                            "active"
                        )
                    )


                    print(
                        "Search query:",
                        search.get(
                            "query"
                        )
                    )


            print(
                "Theme:",
                theme_mode
            )


            # ----------------------------------------------
            # Render SAME picker state across every viewport
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
                        "emoji_sticker_gif_picker",

                    template_name=
                        "emoji_sticker_gif_picker.html",

                    context_key=
                        "picker",

                    page_data=
                        picker,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "emoji_sticker_gif_picker",
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