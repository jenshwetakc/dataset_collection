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

from social_media.email.generators.rules_generator import (
    generate_rules_data,
)

from social_media.email.renderers.common_renderer import (
    render_email_page,
)


# NUM_SAMPLES = 2
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


async def main():

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )


    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch()
        )


        for sample_index in range(
            NUM_SAMPLES
        ):

            rules = (
                generate_rules_data()
            )

            system = (
                generate_system_data()
            )

            theme = (
                generate_theme()
            )


            print(
                f"[EMAIL RULES] "
                f"sample={sample_index} "
                f"state={rules['state']} "
                f"theme={theme['mode']} "
                f"rules={len(rules['rules'])}"
            )


            for viewport in viewports:

                await render_email_page(

                    browser=
                        browser,

                    sample_index=
                        sample_index,

                    page_type=
                        "rules",

                    template_name=
                        "rules.html",

                    context_key=
                        "rules",

                    page_data=
                        rules,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,

                    output_subdir=
                        "rules",

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