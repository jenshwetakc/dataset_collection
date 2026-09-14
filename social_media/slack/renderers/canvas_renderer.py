# social_media/slack/renderers/canvas_renderer.py

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

from social_media.common.common_renderer import (
    resolve_viewports,
)

from social_media.slack.generators.canvas_generator import (
    generate_canvas_data,
)

from social_media.slack.renderers.common_renderer import (
    render_slack_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
VIEWPORT_MODE = "selected"
#
#
# SELECTED_VIEWPORTS = [
#     "small_mobile",
#     "tablet_landscape",
#     "desktop_fhd",
# ]
#
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
#
#     # If already added:
#     # "emoji_only",
# ]
#
#
# THEME_MODE = "random"
#
#
# CAPTURE_FULL_PAGE = True
#
#
# CAPTURE_VIEWPORTS = True
#
#
# SCROLL_PERCENTAGES = [
#     0,
#     10,
#     20,
#     30,
#     40,
#     50,
#     60,
#     70,
#     80,
#     90,
#     100,
# ]
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

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )


        for sample_index in range(
            NUM_SAMPLES
        ):

            canvas = (
                generate_canvas_data()
            )

            system = (
                generate_system_data()
            )

            theme = (
                generate_theme()
            )


            for viewport in viewports:

                print(
                    "[SLACK CANVAS]",
                    "sample=",
                    sample_index,
                    "viewport=",
                    viewport["name"],
                    "theme=",
                    theme["mode"],
                    "panel=",
                    canvas["panel_mode"],
                )


                await render_slack_page(

                    browser=browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "canvas",

                    template_name=
                        "canvas.html",

                    context_key=
                        "canvas",

                    page_data=
                        canvas,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "canvas",

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