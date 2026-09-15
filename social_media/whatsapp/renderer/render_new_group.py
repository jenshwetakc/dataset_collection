import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.new_group_generator import (
    generate_new_group_page,
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

    # ------------------------------------------------------
    # Resolve viewports
    # ------------------------------------------------------

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    print("\nRendering New Group page")
    print("Viewports:")

    for viewport in viewports:

        print(
            f"  {viewport['name']} "
            f"{viewport['width']}x"
            f"{viewport['height']} "
            f"DPR={viewport.get('dpr', 1)}"
        )


    # ------------------------------------------------------
    # Start browser
    # ------------------------------------------------------

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
            # Generate page state ONCE
            # ----------------------------------------------

            new_group = (
                generate_new_group_page()
            )


            # ----------------------------------------------
            # System status ONCE
            # ----------------------------------------------

            system = (
                generate_system_status()
            )


            # ----------------------------------------------
            # Theme ONCE
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
            # Debug information
            # ----------------------------------------------

            print(
                "Theme:",
                theme_mode,
            )

            print(
                "Contacts:",
                new_group["contact_count"],
            )

            print(
                "All contacts:",
                new_group["all_contact_count"],
            )

            print(
                "Selected members:",
                new_group["selected_count"],
            )

            print(
                "Maximum members:",
                new_group["max_members"],
            )

            print(
                "Can continue:",
                new_group["can_continue"],
            )

            print(
                "Selected strip:",
                new_group["show_selected_strip"],
            )

            print(
                "Search active:",
                new_group["search"]["active"],
            )

            print(
                "Search query:",
                new_group["search"]["query"],
            )


            # ----------------------------------------------
            # Render SAME generated state
            # across all selected viewports
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
                        "new_group",

                    template_name=
                        "new_group.html",

                    context_key=
                        "new_group",

                    page_data=
                        new_group,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "new_group",
                )


        # ==================================================
        # Close browser
        # ==================================================

        await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )