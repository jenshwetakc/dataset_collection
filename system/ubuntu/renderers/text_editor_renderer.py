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

from system.ubuntu.generators.text_editor_generator import (
    generate_text_editor_data,
)

from system.ubuntu.renderers.renderer import (
    render_ubuntu_page,
)

from system.ubuntu.generators.system_generator import (
    generate_system_data,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# SELECTED_VIEWPORTS = [
#
#     "small_laptop",
#
#     "desktop_qhd",
# ]

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


THEME_MODE = "random"


# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Theme
# ==========================================================

def generate_theme():

    if THEME_MODE == "random":

        mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

    else:

        mode = THEME_MODE


    return generate_accessible_theme(
        mode=mode
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
                NUM_SAMPLES
            ):

                editor_data = (
                    generate_text_editor_data()
                )


                theme = (
                    generate_theme()
                )


                for viewport in viewports:

                    system_data = (
                        generate_system_data(
                            viewport=
                                viewport
                        )
                    )


                    print(
                        "\n"
                        "=========================================="
                    )

                    print(
                        "UBUNTU TEXT EDITOR"
                    )

                    print(
                        "Sample:",
                        sample_index,
                    )

                    print(
                        "State:",
                        editor_data[
                            "state"
                        ],
                    )

                    print(
                        "Tabs:",
                        len(
                            editor_data[
                                "tabs"
                            ]
                        ),
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
                        "=========================================="
                    )


                    await render_ubuntu_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "text_editor",

                        template_name=
                            "text_editor.html",

                        context_key=
                            "editor",

                        page_data=
                            editor_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            CAPTURE_FULL_PAGE,

                        capture_viewports=
                            CAPTURE_VIEWPORTS,

                        scroll_percentages=
                            SCROLL_PERCENTAGES,
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