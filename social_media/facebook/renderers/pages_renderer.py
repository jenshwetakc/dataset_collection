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

from social_media.facebook.generators.pages_generator import (
    generate_pages_data,
)

from social_media.facebook.renderers.common_renderer import (
    render_facebook_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "desktop_fhd",
# ]
#
#
# # ANNOTATION_PROFILES = [
# #     "big_components",
# #     "components",
# #     "small_elements",
# #     "icons_only",
# # ]
# ANNOTATION_PROFILES = [
#     "big_components",
#     "small_elements",
# ]
#
#
#
# THEME_MODE = "random"
#
#
# CAPTURE_FULL_PAGE = True
#
# CAPTURE_VIEWPORTS = True
#
#
# SCROLL_PERCENTAGES = [
#     0,
#     25,
#     50,
#     75,
#     100,
# ]
NUM_SAMPLES = 30
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

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:

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

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        for sample_index in range(
            NUM_SAMPLES
        ):

            pages_data = (
                generate_pages_data()
            )

            system = (
                generate_system_data()
            )

            theme = (
                generate_theme()
            )

            print(
                "\n"
                "=========================================="
            )

            print(
                "FACEBOOK PAGES SAMPLE",
                sample_index,
            )

            print(
                "=========================================="
            )

            print(
                "State:",
                pages_data[
                    "state"
                ]["name"],
            )

            print(
                "Managed Pages:",
                len(
                    pages_data[
                        "managed_pages"
                    ]
                ),
            )

            print(
                "Discovered Pages:",
                len(
                    pages_data[
                        "discovered_pages"
                    ]
                ),
            )

            for viewport in viewports:

                print(
                    "Rendering:",
                    viewport["name"],
                )

                await render_facebook_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "pages",

                    template_name=
                        "pages.html",

                    context_key=
                        "pages",

                    page_data=
                        pages_data,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "pages",

                    annotation_profiles=
                        ANNOTATION_PROFILES,

                    capture_full_page=
                        CAPTURE_FULL_PAGE,

                    capture_viewports=
                        CAPTURE_VIEWPORTS,

                    scroll_percentages=
                        SCROLL_PERCENTAGES,
                )

        await browser.close()


if __name__ == "__main__":

    asyncio.run(
        main()
    )