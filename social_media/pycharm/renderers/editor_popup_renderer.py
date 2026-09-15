from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.pycharm.generators.editor_popup_generator import (
    POPUP_STATES,
    generate_editor_popup_data,
)

from social_media.pycharm.renderers.common_renderer import (
    render_pycharm_page,
)


# ==========================================================
# Configuration
# ==========================================================

#
NUM_SAMPLES_PER_STATE = 18
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

ANNOTATION_PROFILES = [
    "big_components",
    "icons_only",
]


THEME_MODE = "random"

# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True

# SCROLL_PERCENTAGES = [
#     0,
#     25,
#     50,
#     75,
#     100,
# ]


SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Theme
# ==========================================================

def generate_theme():

    mode = (
        random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        try:

            sample_index = 0

            for popup_state in POPUP_STATES:

                for _ in range(
                    NUM_SAMPLES_PER_STATE
                ):

                    popup_data = (
                        generate_editor_popup_data(
                            state=popup_state
                        )
                    )

                    system = (
                        generate_system_data()
                    )

                    theme = (
                        generate_theme()
                    )

                    for viewport in viewports:

                        await render_pycharm_page(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            page_type=
                                "editor_popup",

                            template_name=
                                "editor_popup.html",

                            context_key=
                                "popup",

                            page_data=
                                popup_data,

                            system=
                                system,

                            theme=
                                theme,

                            viewport=
                                viewport,

                            output_subdir=
                                "editor_popup",

                            annotation_profiles=
                                ANNOTATION_PROFILES,

                            capture_full_page=
                                CAPTURE_FULL_PAGE,

                            capture_viewports=
                                CAPTURE_VIEWPORTS,

                            scroll_percentages=
                                SCROLL_PERCENTAGES,
                        )

                    sample_index += 1

        finally:

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )