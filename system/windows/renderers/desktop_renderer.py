from __future__ import annotations

import asyncio

from playwright.async_api import (
    async_playwright,
)

from system.common.palette_generator import (
    generate_accessible_theme,
)

from system.common.viewport import (
    get_viewports_by_names,
)

from system.windows.generators.desktop_generator import (
    generate_desktop_data,
)

from system.windows.renderers.renderer import (
    render_windows_page,
)

from system.windows.generators.system_generator import (
    generate_system_data,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


SELECTED_VIEWPORTS = [
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




# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
]


# ANNOTATION_PROFILES = [
#
#     "big_components",
#
#     "components",
#
#     "small_elements",
#
#     "icons_only",
# ]
ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODES = [
    "light",
    "dark",
]


# ==========================================================
# Main
# ==========================================================

async def main():

    viewports = (
        get_viewports_by_names(
            SELECTED_VIEWPORTS
        )
    )


    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch()
        )


        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                for viewport in viewports:

                    theme = (
                        generate_accessible_theme(
                            mode=None,
                        )
                    )


                    system = (
                        generate_system_data(
                            viewport=
                                viewport
                        )
                    )


                    desktop = (
                        generate_desktop_data()
                    )


                    print(
                        "\n"
                        "======================================="
                    )

                    print(
                        "WINDOWS DESKTOP"
                    )

                    print(
                        "Sample:",
                        sample_index,
                    )

                    print(
                        "Viewport:",
                        viewport["name"],
                    )

                    print(
                        "Theme:",
                        theme["mode"],
                    )

                    print(
                        "State:",
                        desktop["state"],
                    )


                    await render_windows_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "desktop",

                        template_name=
                            "desktop.html",

                        context_key=
                            "desktop",

                        page_data=
                            desktop,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "desktop",

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            True,

                        capture_viewports=
                            True,

                        scroll_percentages=[
                            0,
                        ],
                    )


        finally:

            await browser.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )