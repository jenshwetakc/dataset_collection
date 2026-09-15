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

from system.windows.generators.notepad_generator import (
    NOTEPAD_STATES,
    generate_notepad_data,
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
        NOTEPAD_STATES
    ):

        return NOTEPAD_STATES[
            sample_index
        ]

    return random.choice(
        NOTEPAD_STATES
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

                state = choose_state(
                    sample_index
                )


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


                notepad = (
                    generate_notepad_data(
                        state=
                            state
                    )
                )


                print(
                    "\n"
                    "========================================"
                )

                print(
                    "WINDOWS NOTEPAD"
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
                        "notepad",

                    template_name=
                        "notepad.html",

                    context_key=
                        "notepad",

                    page_data=
                        notepad,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "notepad",

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