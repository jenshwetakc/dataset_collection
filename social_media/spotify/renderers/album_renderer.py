from __future__ import annotations

import asyncio

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.renderer import (
    resolve_viewports,
)

from social_media.spotify.generators.album_generator import (
    generate_album_page,
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

# NUM_SAMPLES = 5
#
#
# # ==========================================================
# # Viewports
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
#
#
# # ==========================================================
# # Themes
# # ==========================================================
#
THEME_MODES = [
    "light",
    "dark",
]
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


# THEME_MODES = "random"

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
# Main
# ==========================================================

async def main() -> None:

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

                # ==========================================
                # Logical Screen
                # ==========================================

                album_data = (
                    generate_album_page()
                )


                system = (
                    generate_system_data()
                )


                # ==========================================
                # Theme Pair
                # ==========================================

                for theme_mode in (
                    THEME_MODES
                ):

                    theme = (
                        generate_accessible_theme(
                            mode=theme_mode
                        )
                    )


                    print(
                        "\n"
                        "=========================================="
                    )

                    print(
                        f"Spotify Album Sample: "
                        f"{sample_index}"
                    )

                    print(
                        f"Album: "
                        f"{album_data['album']['name']}"
                    )

                    print(
                        f"Artist: "
                        f"{album_data['album']['artist']}"
                    )

                    print(
                        f"Tracks: "
                        f"{len(album_data['tracks'])}"
                    )

                    print(
                        f"Theme: "
                        f"{theme_mode}"
                    )

                    print(
                        f"Time: "
                        f"{system['time_text']}"
                    )

                    print(
                        "=========================================="
                    )


                    # ======================================
                    # Every Viewport
                    # ======================================

                    for viewport in viewports:

                        await render_spotify_page(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            page_type=
                                "album",

                            template_name=
                                "album.html",

                            context_key=
                                "album",

                            page_data=
                                album_data,

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