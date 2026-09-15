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

from social_media.canva.generators.brand_kit_generator import (
    BRAND_STATES,
    generate_brand_kit_data,
)

from social_media.canva.renderers.common_renderer import (
    render_canva_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 1


# SELECTED_VIEWPORTS = [
#     "small_mobile",
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
# Theme
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

            sample_index = 0


            # ==================================================
            # Render every state explicitly
            # ==================================================

            for state in BRAND_STATES:

                for _ in range(
                    NUM_SAMPLES_PER_STATE
                ):

                    sample_index += 1


                    brand_data = (
                        generate_brand_kit_data(
                            forced_state=state
                        )
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
                            "CANVA BRAND KIT"
                        )

                        print(
                            "Sample:",
                            sample_index,
                        )

                        print(
                            "State:",
                            state,
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
                            "Brand:",
                            brand_data[
                                "brand"
                            ][
                                "name"
                            ],
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
                                f"brand_kit_{state}",

                            template_name=
                                "brand_kit.html",

                            context_key=
                                "brand_kit",

                            page_data=
                                brand_data,

                            system=
                                system_data,

                            theme=
                                theme,

                            viewport=
                                viewport,

                            output_subdir=
                                f"brand_kit/{state}",

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