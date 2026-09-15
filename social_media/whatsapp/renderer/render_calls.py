import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.whatsapp.generators.calls_generator import (
    generate_calls_page,
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

    print(
        "\nRendering Calls page"
    )

    print(
        "Viewports:"
    )

    for viewport in viewports:

        print(
            f"  {viewport['name']} | "
            f"{viewport['category']} | "
            f"{viewport.get('orientation', 'unknown')} | "
            f"{viewport['width']}x{viewport['height']} | "
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
            # Generate page content ONCE
            # ----------------------------------------------

            calls = (
                generate_calls_page()
            )

            # ----------------------------------------------
            # Generate status bar ONCE
            # ----------------------------------------------

            system = (
                generate_system_status()
            )

            # ----------------------------------------------
            # Light / Dark mode ONCE
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

            print(
                "Theme:",
                theme_mode
            )

            if "call_count" in calls:
                print(
                    "Call count:",
                    calls["call_count"]
                )

            if "missed_count" in calls:
                print(
                    "Missed calls:",
                    calls["missed_count"]
                )

            if "show_favorites" in calls:
                print(
                    "Show favorites:",
                    calls["show_favorites"]
                )

            # ----------------------------------------------
            # Render SAME page content across viewports
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
                        "calls",

                    template_name=
                        "calls.html",

                    context_key=
                        "calls",

                    page_data=
                        calls,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "calls",
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