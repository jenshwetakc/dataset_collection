import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.updates_generator import (
    generate_updates_page,
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


# Used only when:
#
# VIEWPORT_MODE = "selected"
#
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


    print(
        "\nRendering viewports:"
    )

    for viewport in viewports:

        print(
            f"  {viewport['name']} "
            f"{viewport['width']}x"
            f"{viewport['height']} "
            f"DPR={viewport.get('dpr', 1)}"
        )


    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )


        output_index = 1


        for _ in range(
            NUM_SAMPLES
        ):

            # ==================================================
            # Generate one Updates page state
            # ==================================================

            updates = (
                generate_updates_page()
            )


            system = (
                generate_system_status()
            )


            # ==================================================
            # Theme
            # ==================================================

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


            # ==================================================
            # Render same state across selected viewports
            # ==================================================

            for viewport in viewports:

                await render_page(

                    browser=
                        browser,

                    sample_index=
                        output_index,

                    page_type=
                        "updates",

                    template_name=
                        "updates.html",

                    context_key=
                        "updates",

                    page_data=
                        updates,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "updates",
                )


                output_index += 1


        await browser.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )