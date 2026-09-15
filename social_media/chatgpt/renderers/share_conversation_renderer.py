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
    get_all_viewports,
    get_random_viewport,
    get_viewports_by_names,
)

from social_media.chatgpt.generators.share_conversation_generator import (
    generate_share_conversation_data,
)

from social_media.chatgpt.renderers.common_renderer import (
    render_chatgpt_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Viewports
# ==========================================================

VIEWPORT_MODE = "selected"


# SELECTED_VIEWPORTS = [
#
#     "small_mobile",
#
#     "standard_android",
#
#     "standard_iphone",
#
#     "large_mobile",
#
#     "mobile_landscape",
#
#     "tablet_portrait",
#
#     "tablet_landscape",
#
#     "small_laptop",
#
#     "laptop",
#
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



# ==========================================================
# Annotation Profiles
# ==========================================================

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

# ==========================================================
# Theme
# ==========================================================

THEME_MODE = "random"


# ==========================================================
# Capture
# ==========================================================

# CAPTURE_FULL_PAGE = True
CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True


# Modal screen has no meaningful page scrolling.
SCROLL_PERCENTAGES = [
    0,
]


# ==========================================================
# Theme Resolver
# ==========================================================

def resolve_theme_mode() -> str:

    if THEME_MODE == "random":

        return random.choice([
            "light",
            "dark",
        ])

    if THEME_MODE in {
        "light",
        "dark",
    }:

        return THEME_MODE

    raise ValueError(
        f"Unknown THEME_MODE: "
        f"{THEME_MODE}"
    )


# ==========================================================
# Viewport Resolver
# ==========================================================

def resolve_viewports():

    if VIEWPORT_MODE == "all":

        return get_all_viewports()

    if VIEWPORT_MODE == "selected":

        return get_viewports_by_names(
            SELECTED_VIEWPORTS
        )

    if VIEWPORT_MODE == "random":

        return [
            get_random_viewport()
        ]

    raise ValueError(
        f"Unknown VIEWPORT_MODE: "
        f"{VIEWPORT_MODE}"
    )


# ==========================================================
# Render
# ==========================================================

async def render_samples():

    viewports = (
        resolve_viewports()
    )


    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch(
                headless=True,
            )
        )


        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                share_data = (
                    generate_share_conversation_data()
                )


                system = (
                    generate_system_data()
                )


                theme = (
                    generate_accessible_theme(
                        mode=
                            resolve_theme_mode()
                    )
                )


                for viewport in viewports:

                    await render_chatgpt_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "share_conversation",

                        template_name=
                            "share_conversation.html",

                        context_key=
                            "share_page",

                        page_data=
                            share_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "share_conversation",

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
# Main
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        render_samples()
    )