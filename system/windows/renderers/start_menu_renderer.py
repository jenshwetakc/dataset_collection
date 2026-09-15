from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from system.common.palette_generator import (
    generate_accessible_theme,
)

from system.common.viewport import (
    get_viewports_by_names,
)

from system.windows.renderers.renderer import (
    render_windows_page,
)

from system.windows.generators.start_menu_generator import (
    START_MENU_STATES,
    generate_start_menu_data,
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


THEME_MODE = "random"


# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
]

# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
# ]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
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

                viewport = random.choice(
                    viewports
                )


                theme = (
                    generate_accessible_theme(
                        mode=None
                    )
                )


                system = (
                    generate_system_data(
                        viewport=
                            viewport
                    )
                )


                # --------------------------------------------------
                # Cycle through all states first.
                #
                # This ensures state diversity instead of relying
                # entirely on random selection.
                # --------------------------------------------------

                state = (
                    START_MENU_STATES[
                        sample_index
                        % len(
                            START_MENU_STATES
                        )
                    ]
                )


                start_menu = (
                    generate_start_menu_data(
                        state=
                            state
                    )
                )


                print(
                    "\n"
                    "======================================="
                )

                print(
                    "WINDOWS START MENU"
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
                    start_menu["state"],
                )


                await render_windows_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "start_menu",

                    template_name=
                        "start_menu.html",

                    context_key=
                        "start_menu",

                    page_data=
                        start_menu,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "start_menu",

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