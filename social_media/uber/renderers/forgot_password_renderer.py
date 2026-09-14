from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.common_renderer import (
    resolve_viewports,
)

from social_media.uber.generators.auth_generator import (
    generate_forgot_password_data,
)

from social_media.uber.renderers.common_renderer import (
    render_uber_page,
)


# NUM_SAMPLES = 3

VIEWPORT_MODE = "selected"
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     # "tablet_portrait",
#     # "laptop",
#     "desktop_fhd",
# ]
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     # "components",
#     "small_elements",
#     # "icons_only",
# ]
#
# THEME_MODE = "random"
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

def generate_system_data() -> dict:

    return {

        "status_bar_variant":
            "standard",

        "time_text":
            f"{random.randint(0,23):02d}:{random.randint(0,59):02d}",

        "notifications": {
            "icons": [],
        },

        "system_states":
            [],

        "cellular": {
            "available": True,
            "level": random.randint(2, 4),
            "type": "5G",
        },

        "wifi": {
            "connected": True,
            "level": random.randint(1, 3),
        },

        "battery": {
            "level": random.randint(30, 100),
            "charging": False,
            "battery_saver": False,
        },
    }


def generate_theme() -> dict:

    return generate_accessible_theme(

        mode=random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )


async def main():

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
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

                page_data = (
                    generate_forgot_password_data()
                )

                system = (
                    generate_system_data()
                )

                theme = (
                    generate_theme()
                )


                for viewport in viewports:

                    await render_uber_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "forgot_password",

                        template_name=
                            "forgot_password.html",

                        context_key=
                            "forgot_password",

                        page_data=
                            page_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        annotation_profiles=
                            ANNOTATION_PROFILES,

                        capture_full_page=
                            True,

                        capture_viewports=
                            True,
                    )


        finally:

            await browser.close()


if __name__ == "__main__":

    asyncio.run(
        main()
    )