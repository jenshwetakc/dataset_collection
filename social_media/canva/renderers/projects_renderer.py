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

from social_media.canva.generators.projects_generator import (
    generate_projects_data,
)

from social_media.canva.renderers.common_renderer import (
    render_canva_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# SELECTED_VIEWPORTS = [
#     "standard_iphone",
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

THEME_MODE = "random"


# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


SCROLL_PERCENTAGES = [
    0,
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
]


# ==========================================================
# Theme Resolver
# ==========================================================

def resolve_theme_mode() -> str:

    if THEME_MODE == "random":

        return random.choice(
            [
                "light",
                "dark",
            ]
        )

    if THEME_MODE in {
        "light",
        "dark",
    }:

        return THEME_MODE

    raise ValueError(
        "THEME_MODE must be "
        "'light', 'dark', or 'random'."
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

            for sample_index in range(
                1,
                NUM_SAMPLES + 1,
            ):

                project_data = (
                    generate_projects_data()
                )

                system_data = (
                    generate_system_data()
                )


                for viewport in viewports:

                    theme_mode = (
                        resolve_theme_mode()
                    )

                    theme = (
                        generate_accessible_theme(
                            mode=theme_mode
                        )
                    )


                    print(
                        "\n"
                        "=================================="
                    )

                    print(
                        "CANVA PROJECTS"
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
                        theme_mode,
                    )

                    print(
                        "View mode:",
                        project_data["view_mode"],
                    )

                    print(
                        "=================================="
                    )


                    await render_canva_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "projects",

                        template_name=
                            "projects.html",

                        context_key=
                            "projects",

                        page_data=
                            project_data,

                        system=
                            system_data,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "projects",

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