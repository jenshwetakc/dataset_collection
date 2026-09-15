from __future__ import annotations

import asyncio

from playwright.async_api import (
    async_playwright,
)

from social_media.amazon.generators.cart_generator import (
    generate_cart_data,
)

from social_media.amazon.renderers.common_renderer import (
    render_amazon_page,
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


CAPTURE_FULL_PAGE = True


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

    if THEME_MODE == "light":

        return generate_accessible_theme(
            mode="light"
        )

    if THEME_MODE == "dark":

        return generate_accessible_theme(
            mode="dark"
        )

    return generate_accessible_theme()


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
                NUM_SAMPLES
            ):

                amazon = generate_cart_data()

                system = generate_system_data()

                theme = generate_theme()


                print(
                    "\n"
                    "=========================================="
                )

                print(
                    "AMAZON CART SAMPLE",
                    sample_index,
                )

                print(
                    "=========================================="
                )

                print(
                    "State:",
                    amazon["state"],
                )

                print(
                    "Items:",
                    len(
                        amazon["items"]
                    ),
                )

                print(
                    "Saved:",
                    len(
                        amazon["saved_items"]
                    ),
                )

                print(
                    "Total:",
                    amazon["totals"]["total"],
                )


                for viewport in viewports:

                    print(
                        "Rendering:",
                        viewport["name"],
                    )


                    await render_amazon_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "cart",

                        template_name=
                            "cart.html",

                        context_key=
                            "amazon",

                        page_data=
                            amazon,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "cart",

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