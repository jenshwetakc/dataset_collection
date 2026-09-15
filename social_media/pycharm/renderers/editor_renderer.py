from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.pycharm.generators.editor_generator import (
    generate_editor_data,
)

from social_media.pycharm.renderers.common_renderer import (
    render_pycharm_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 1
#
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "desktop_fhd",
# ]
#
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
# ]
#
#
# THEME_MODE = "random"
#
#
# CAPTURE_FULL_PAGE = True
#
# CAPTURE_VIEWPORTS = True
NUM_SAMPLES = 18
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

# IDE screens themselves do not naturally document-scroll.
# One viewport capture is therefore sufficient.
SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Theme
# ==========================================================

def generate_editor_theme():

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
# Render
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

            for sample_index in range(
                NUM_SAMPLES
            ):

                editor_data = (
                    generate_editor_data()
                )

                system = (
                    generate_system_data()
                )

                theme = (
                    generate_editor_theme()
                )

                for viewport in viewports:

                    await render_pycharm_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "editor",

                        template_name=
                            "editor.html",

                        context_key=
                            "editor",

                        page_data=
                            editor_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "editor",

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
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )