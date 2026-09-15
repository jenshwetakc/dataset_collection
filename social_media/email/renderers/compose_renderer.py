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

from social_media.email.generators.compose_generator import (
    generate_compose_data,
)

from social_media.email.renderers.common_renderer import (
    render_email_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 2
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "tablet_portrait",
#     "laptop",
#     "desktop_fhd",
# ]
#
# # ANNOTATION_PROFILES = [
# #     "big_components",
# #     "components",
# #     "small_elements",
# #     "icons_only",
# # ]
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "small_elements",
# ]
#
#
# THEME_MODE = "random"
#
# CAPTURE_FULL_PAGE = True
# CAPTURE_VIEWPORTS = True
#
# SCROLL_PERCENTAGES = [
#     0,
#     25,
#     50,
#     75,
#     100,
# ]
NUM_SAMPLES = 40
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

    mode = (
        random.choice([
            "light",
            "dark",
        ])
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

        browser = await playwright.chromium.launch()

        for sample_index in range(
            NUM_SAMPLES
        ):

            compose = generate_compose_data()

            system = generate_system_data()

            theme = generate_theme()

            print(
                f"[EMAIL COMPOSE] "
                f"sample={sample_index} "
                f"state={compose['state']} "
                f"theme={theme['mode']} "
                f"recipients={len(compose['recipients'])} "
                f"attachments={len(compose['attachments'])}"
            )

            for viewport in viewports:

                await render_email_page(
                    browser=browser,
                    sample_index=sample_index,
                    page_type="compose",
                    template_name="compose.html",
                    context_key="compose",
                    page_data=compose,
                    system=system,
                    theme=theme,
                    viewport=viewport,
                    output_subdir="compose",
                    annotation_profiles=ANNOTATION_PROFILES,
                    capture_full_page=CAPTURE_FULL_PAGE,
                    capture_viewports=CAPTURE_VIEWPORTS,
                    scroll_percentages=SCROLL_PERCENTAGES,
                )

        await browser.close()


if __name__ == "__main__":

    asyncio.run(
        main()
    )
