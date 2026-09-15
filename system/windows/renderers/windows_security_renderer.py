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

from system.windows.generators.system_generator import (
    generate_system_data,
)

from system.windows.generators.windows_security_generator import (
    WINDOWS_SECURITY_STATES,
    generate_windows_security_data,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SCREENS = 50


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
# State Selection
# ==========================================================

def choose_state(
    sample_index: int,
) -> str:

    if sample_index < len(
        WINDOWS_SECURITY_STATES
    ):

        return (
            WINDOWS_SECURITY_STATES[
                sample_index
            ]
        )


    return random.choice(
        WINDOWS_SECURITY_STATES
    )


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
                NUM_SCREENS
            ):

                viewport = random.choice(
                    viewports
                )


                state = choose_state(
                    sample_index
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


                windows_security = (
                    generate_windows_security_data(
                        state=
                            state
                    )
                )


                print(
                    "\n"
                    "======================================="
                )

                print(
                    "WINDOWS SECURITY"
                )

                print(
                    "Screen:",
                    sample_index + 1,
                    "/",
                    NUM_SCREENS,
                )

                print(
                    "State:",
                    state,
                )

                print(
                    "Viewport:",
                    viewport[
                        "name"
                    ],
                )

                print(
                    "Theme:",
                    theme[
                        "mode"
                    ],
                )

                print(
                    "Wallpaper:",
                    bool(
                        system[
                            "wallpaper"
                        ]
                    ),
                )


                await render_windows_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "windows_security",

                    template_name=
                        "windows_security.html",

                    context_key=
                        "windows_security",

                    page_data=
                        windows_security,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "windows_security",

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


if __name__ == "__main__":

    asyncio.run(
        main()
    )