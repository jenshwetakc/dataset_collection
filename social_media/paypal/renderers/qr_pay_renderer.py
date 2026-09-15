from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.paypal.generators.qr_pay_generator import (
    generate_qr_pay_data,
)

from social_media.paypal.renderers.common_renderer import (
    render_paypal_page,
)


# ==========================================================
# Configuration
# ==========================================================

# NUM_SAMPLES = 3
#
#
# VIEWPORTS = [
#     "standard_iphone",
#     # "tablet_portrait",
#     "laptop",
#     "desktop_fhd",
# ]
#
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
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
VIEWPORTS = [
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

    mode = (
        random.choice([
            "light",
            "dark",
        ])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode,
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    viewports = (
        get_viewports_by_names(
            VIEWPORTS
        )
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

                qr = (
                    generate_qr_pay_data()
                )

                theme = (
                    generate_theme()
                )

                system = (
                    generate_system_data()
                )


                for viewport in viewports:

                    print(
                        "\n"
                        "========================================"
                    )

                    print(
                        "PayPal QR Pay"
                    )

                    print(
                        "Sample:",
                        sample_index
                    )

                    print(
                        "Viewport:",
                        viewport["name"]
                    )

                    print(
                        "Theme:",
                        theme["mode"]
                    )

                    print(
                        "Mode:",
                        qr["active_mode"]
                    )

                    print(
                        "Permission dialog:",
                        qr[
                            "show_permission_dialog"
                        ]
                    )

                    print(
                        "========================================"
                    )


                    await render_paypal_page(

                        browser=
                            browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "qr_pay",

                        template_name=
                            "qr_pay.html",

                        context_key=
                            "qr",

                        page_data=
                            qr,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        output_subdir=
                            "qr_pay",

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
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )