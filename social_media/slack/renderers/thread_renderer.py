# social_media/slack/renderers/thread_renderer.py

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

from social_media.slack.generators.thread_generator import (
    generate_thread_data,
)

from social_media.slack.renderers.common_renderer import (
    render_slack_page,
)


# ==========================================================
# Configuration
# ==========================================================
#
# NUM_SAMPLES = 3
#
#
VIEWPORT_MODE = "selected"
#
#
# SELECTED_VIEWPORTS = [
#
#     "small_mobile",
#
#     "tablet_portrait",
#
#     "laptop",
#
#     "desktop_fhd",
#
# ]
#
#
# ANNOTATION_PROFILES = [
#
#     "big_components",
#
#     "components",
#
#     "small_elements",
#
#     "icons_only",
#
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
#
#     0,
#
#     10,
#
#     20,
#
#     30,
#
#     40,
#
#     50,
#
#     60,
#
#     70,
#
#     80,
#
#     90,
#
#     100,
#
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

        mode=
            VIEWPORT_MODE,

        selected=
            SELECTED_VIEWPORTS,
    )


    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )


        for sample_index in range(
            NUM_SAMPLES
        ):

            thread_page = (
                generate_thread_data()
            )

            system = (
                generate_system_data()
            )

            theme = (
                generate_theme()
            )


            for viewport in viewports:

                print(
                    "[SLACK THREAD]",
                    "sample=",
                    sample_index,
                    "viewport=",
                    viewport["name"],
                    "theme=",
                    theme["mode"],
                    "replies=",
                    thread_page[
                        "thread"
                    ][
                        "reply_count"
                    ],
                )


                await render_slack_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "thread",

                    template_name=
                        "thread.html",

                    context_key=
                        "thread_page",

                    page_data=
                        thread_page,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "thread",

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


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )