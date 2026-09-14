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

from social_media.spotify.generators.podcast_generator import (
    generate_podcast_page,
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
# THEME_MODES = [
#     "light",
#     "dark",
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


# THEME_MODES = "random"
THEME_MODES = [
    "light",
    "dark",
]
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
                # One Logical Podcast Page
                # ==========================================

                podcast_data = (
                    generate_podcast_page()
                )


                system = (
                    generate_system_data()
                )


                # ==========================================
                # Light / Dark Pair
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
                        f"Spotify Podcast Sample: "
                        f"{sample_index}"
                    )

                    print(
                        f"Show: "
                        f"{podcast_data['show']['name']}"
                    )

                    print(
                        f"Episodes: "
                        f"{len(podcast_data['episodes'])}"
                    )

                    print(
                        f"Theme: "
                        f"{theme_mode}"
                    )

                    print(
                        "=========================================="
                    )


                    # ======================================
                    # Render Viewports
                    # ======================================

                    for viewport in viewports:

                        await render_spotify_page(

                            browser=
                                browser,

                            sample_index=
                                sample_index,

                            page_type=
                                "podcast",

                            template_name=
                                "podcast.html",

                            context_key=
                                "podcast",

                            page_data=
                                podcast_data,

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