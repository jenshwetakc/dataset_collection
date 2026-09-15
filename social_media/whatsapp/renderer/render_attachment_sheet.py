import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.attachment_sheet_generator import (
    generate_attachment_sheet_page,
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
        "\nRendering Attachment Sheet"
    )

    print(
        "Viewports:"
    )


    for viewport in viewports:

        print(
            f"  {viewport['name']} | "
            f"{viewport['category']} | "
            f"{viewport['orientation']} | "
            f"{viewport['size_class']} | "
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
            # Generate ONE attachment state
            #
            # Same content is reused across all viewports.
            # ----------------------------------------------

            attachment = (
                generate_attachment_sheet_page()
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
                "Actions:",
                attachment[
                    "action_count"
                ]
            )

            print(
                "Recent media:",
                attachment[
                    "recent_media_count"
                ]
            )

            print(
                "Show recent media:",
                attachment[
                    "show_recent_media"
                ]
            )

            print(
                "Show close:",
                attachment[
                    "show_close"
                ]
            )

            print(
                "Theme:",
                theme_mode
            )


            # ----------------------------------------------
            # Render SAME state across all viewports
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
                        "attachment_sheet",

                    template_name=
                        "attachment_sheet.html",

                    context_key=
                        "attachment",

                    page_data=
                        attachment,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "attachment_sheet",
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