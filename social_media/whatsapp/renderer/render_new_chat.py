import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.new_chat_generator import (
    generate_new_chat_page,
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
# Viewports
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

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    print("\nRendering New Chat page")
    print("Viewports:")

    for viewport in viewports:

        print(
            f"  {viewport['name']} "
            f"{viewport['width']}x"
            f"{viewport['height']} "
            f"DPR={viewport.get('dpr', 1)}"
        )


    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
        )


        # ==================================================
        # Samples
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
            # Generate page ONCE
            # ----------------------------------------------

            new_chat = (
                generate_new_chat_page()
            )


            # ----------------------------------------------
            # System status
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
                    mode=theme_mode,
                )
            )


            # ----------------------------------------------
            # Debug
            # ----------------------------------------------

            print(
                "Theme:",
                theme_mode,
            )

            print(
                "Contacts:",
                new_chat["contact_count"],
            )

            print(
                "Total contacts:",
                new_chat["all_contact_count"],
            )

            print(
                "Groups:",
                len(
                    new_chat["groups"]
                ),
            )

            print(
                "Actions:",
                len(
                    new_chat["actions"]
                ),
            )

            print(
                "Search active:",
                new_chat["search"]["active"],
            )

            print(
                "Search query:",
                new_chat["search"]["query"],
            )


            # ----------------------------------------------
            # Same generated content for every viewport
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
                        "new_chat",

                    template_name=
                        "new_chat.html",

                    context_key=
                        "new_chat",

                    page_data=
                        new_chat,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "new_chat",
                )


        await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )