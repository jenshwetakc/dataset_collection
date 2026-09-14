from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.renderer import (
    resolve_viewports,
)

from social_media.spotify.generators.home_generator import (
    generate_home_page,
)

from social_media.spotify.generators.system_generator import (
    generate_system_data,
)

from social_media.spotify.renderers.common_renderer import (
    render_spotify_page,
)


# ==========================================================
# Configuration
# ==========================================================
#
# NUM_SAMPLES = 3
#
#
# # ==========================================================
# # Viewport Configuration
# # ==========================================================
#
VIEWPORT_MODE = "selected"
#
#
# SELECTED_VIEWPORTS = [
#     "standard_iphone",
#     "tablet_portrait",
#     "laptop",
#     "desktop_fhd",
# ]
#
#
# # ==========================================================
# # Annotation Profiles
# # ==========================================================
#
# ANNOTATION_PROFILES = [
#     "big_components",
#     "components",
#     "small_elements",
#     "icons_only",
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


THEME_MODES = "random"

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
# Theme Configuration
# ==========================================================

THEME_MODE = "random"


def generate_spotify_theme() -> dict:

    if THEME_MODE == "random":

        selected_mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

    elif THEME_MODE in {
        "light",
        "dark",
    }:

        selected_mode = THEME_MODE

    else:

        raise ValueError(
            f"Unknown THEME_MODE: "
            f"{THEME_MODE}"
        )

    return generate_accessible_theme(
        mode=selected_mode
    )


# ==========================================================
# Main
# ==========================================================

async def main() -> None:

    # ------------------------------------------------------
    # Resolve viewports once
    # ------------------------------------------------------

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        try:

            for sample_index in range(
                NUM_SAMPLES
            ):

                # ==================================================
                # Generate ONE logical Spotify screen
                #
                # This content is reused for every viewport.
                # ==================================================

                home_data = (
                    generate_home_page()
                )


                # ==================================================
                # Generate ONE system state
                #
                # Shared status-bar state:
                # - time
                # - notifications
                # - Wi-Fi
                # - cellular
                # - battery
                # - system icons
                #
                # Reused across every viewport for this sample.
                # ==================================================

                system = (
                    generate_system_data()
                )


                # ==================================================
                # Theme
                # ==================================================

                theme = (
                    generate_spotify_theme()
                )


                # ==================================================
                # Debug
                # ==================================================

                print(
                    "\n"
                    "=========================================="
                )

                print(
                    f"Spotify Home Sample: "
                    f"{sample_index}"
                )

                print(
                    f"Theme: "
                    f"{theme['mode']}"
                )

                print(
                    f"Seed: "
                    f"{theme['seed']}"
                )

                print(
                    f"Time: "
                    f"{system['time_text']}"
                )

                print(
                    f"Status Bar: "
                    f"{system['status_bar_variant']}"
                )

                print(
                    f"Notifications: "
                    f"{system['notifications']['count']}"
                )

                print(
                    f"Battery: "
                    f"{system['battery']['level']}%"
                )

                print(
                    "=========================================="
                )


                # ==================================================
                # Render same logical screen at every viewport
                # ==================================================

                for viewport in viewports:

                    await render_spotify_page(

                        browser=browser,

                        sample_index=
                            sample_index,

                        page_type=
                            "home",

                        template_name=
                            "home.html",

                        context_key=
                            "home",

                        page_data=
                            home_data,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,

                        annotation_profiles=
                            ANNOTATION_PROFILES,
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