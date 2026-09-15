import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.storage_manager_generator import (
    generate_storage_manager_page,
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


    print("\nRendering Storage Manager")
    print("Viewports:")

    for viewport in viewports:

        print(
            f"  {viewport['name']} "
            f"{viewport['width']}x"
            f"{viewport['height']} "
            f"DPR={viewport.get('dpr', 1)}"
        )


    # ------------------------------------------------------
    # Start Playwright
    # ------------------------------------------------------

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
        )


        # ==================================================
        # Generate samples
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

            storage_manager = (
                generate_storage_manager_page()
            )


            # ----------------------------------------------
            # Generate system status ONCE
            # ----------------------------------------------

            system = (
                generate_system_status()
            )


            # ----------------------------------------------
            # Generate theme ONCE
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
            # Debug output
            # ----------------------------------------------

            print(
                "Theme:",
                theme_mode,
            )

            print(
                "Used:",
                storage_manager["storage"]["used_gb"],
                "GB",
            )

            print(
                "Free:",
                storage_manager["storage"]["free_gb"],
                "GB",
            )

            print(
                "Total:",
                storage_manager["storage"]["total_gb"],
                "GB",
            )

            print(
                "Usage:",
                storage_manager["storage"]["used_percent"],
                "%",
            )

            print(
                "Categories:",
                storage_manager["category_count"],
            )

            print(
                "Chats:",
                storage_manager["chat_count"],
            )


            # ----------------------------------------------
            # Render same generated page
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
                        "storage_manager",

                    template_name=
                        "storage_manager.html",

                    context_key=
                        "storage_manager",

                    page_data=
                        storage_manager,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "storage_manager",
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