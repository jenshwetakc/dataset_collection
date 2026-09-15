from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from tqdm import tqdm

from social_media.youtube.renderers.common_renderer import (
    render_page,
    resolve_viewports,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.youtube.generators.settings_generator import (
    SETTINGS_SECTIONS,
    generate_settings_page,
)


# ==========================================================
# Paths
# ==========================================================

YOUTUBE_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = (
    YOUTUBE_ROOT
    / "templates"
)

OUTPUT_ROOT = (
    YOUTUBE_ROOT
    / "output"
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 50


# ==========================================================
# Settings Sections
# ==========================================================

SETTINGS_SECTIONS_TO_RENDER = [
    "account",
    "notifications",
    "playback",
    "downloads",
    "privacy",
    "connected_apps",
    "billing",
    "advanced",
]


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODES = [
    "light",
    "dark",
]


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORT_MODE = "selected"

SELECTED_VIEWPORTS = [
    "standard_iphone",
    "tablet_landscape",
    "laptop",
    "desktop_fhd",
]

# ==========================================================
# Scroll Configuration
# ==========================================================

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]


# ==========================================================
# Capture Configuration
# ==========================================================

SAVE_FULL_PAGE = True

SAVE_VIEWPORTS = True


# ==========================================================
# Validation
# ==========================================================

def validate_settings_sections() -> None:

    available_sections = {
        section["id"]
        for section in SETTINGS_SECTIONS
    }

    unknown_sections = [
        section
        for section in SETTINGS_SECTIONS_TO_RENDER
        if section not in available_sections
    ]

    if unknown_sections:

        raise ValueError(
            "Unknown settings sections: "
            f"{unknown_sections}. "
            f"Available sections: "
            f"{sorted(available_sections)}"
        )


# ==========================================================
# Debug
# ==========================================================

def print_page_debug(
    page: dict,
) -> None:

    print(
        f"Selected section: "
        f"{page['selected_section']}"
    )

    print(
        f"Title: "
        f"{page['content']['title']}"
    )

    print(
        f"Groups: "
        f"{len(page['content']['groups'])}"
    )

    print(
        f"User: "
        f"{page['user']['name']}"
    )

    print(
        "Groups:"
    )

    for group in page["content"]["groups"]:

        print(
            f"  - "
            f"{group['title']}"
            f" | "
            f"type={group['type']}"
        )

        if (
            group["type"]
            in {
                "settings",
                "apps",
            }
        ):

            items = (
                group.get(
                    "items",
                    [],
                )
            )

            print(
                f"    items: "
                f"{len(items)}"
            )


# ==========================================================
# Main
# ==========================================================

async def main():

    # ======================================================
    # Validate Configuration
    # ======================================================

    validate_settings_sections()


    # ======================================================
    # Resolve Viewports
    # ======================================================

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )


    # ======================================================
    # Configuration Debug
    # ======================================================

    print(
        "\n"
        "=========================================="
    )

    print(
        "YOUTUBE SETTINGS"
    )

    print(
        "=========================================="
    )

    print(
        f"Samples: "
        f"{NUM_SAMPLES}"
    )

    print(
        f"Settings sections: "
        f"{SETTINGS_SECTIONS_TO_RENDER}"
    )

    print(
        f"Themes: "
        f"{THEME_MODES}"
    )

    print(
        f"Full-page capture: "
        f"{SAVE_FULL_PAGE}"
    )

    print(
        f"Viewport capture: "
        f"{SAVE_VIEWPORTS}"
    )

    print(
        f"Scroll positions: "
        f"{SCROLL_PERCENTAGES}"
    )

    print(
        "\nTesting viewports:"
    )

    for viewport in viewports:

        orientation = (
            "landscape"
            if viewport["width"]
            > viewport["height"]
            else "portrait"
        )

        print(
            f"  - "
            f"{viewport['name']}"
            f" | "
            f"{viewport['width']}"
            f"x"
            f"{viewport['height']}"
            f" | "
            f"{orientation}"
            f" | "
            f"DPR="
            f"{viewport.get('dpr', 1)}"
        )


    # ======================================================
    # Playwright
    # ======================================================

    async with async_playwright() as p:

        browser = (
            await p.chromium.launch(
                headless=True
            )
        )


        # ==================================================
        # Sample Loop
        # ==================================================

        for sample_index in tqdm(
            range(NUM_SAMPLES),
            desc="YouTube Settings",
        ):

            print(
                "\n"
                "------------------------------------------"
            )

            print(
                f"Sample: "
                f"{sample_index}"
            )


            # ==============================================
            # Settings Section Loop
            # ==============================================

            for selected_section in (
                SETTINGS_SECTIONS_TO_RENDER
            ):

                # ==========================================
                # Generate Section ONCE
                #
                # The same generated data is reused across:
                #
                # - light
                # - dark
                # - mobile
                # - tablet
                # - laptop
                # - desktop
                #
                # This is important for controlled visual
                # comparison.
                # ==========================================

                settings_page = (
                    generate_settings_page(
                        selected_section=
                            selected_section
                    )
                )


                print(
                    "\n"
                    "======================================"
                )

                print(
                    f"Settings section: "
                    f"{selected_section}"
                )

                print_page_debug(
                    settings_page
                )


                # ==========================================
                # Theme Loop
                # ==========================================

                for theme_mode in THEME_MODES:

                    theme = (
                        generate_accessible_theme(
                            mode=theme_mode
                        )
                    )


                    print(
                        "\n"
                        f"Theme: "
                        f"{theme_mode}"
                    )

                    print(
                        f"Seed: "
                        f"{theme.get('seed')}"
                    )

                    print(
                        f"WCAG pass: "
                        f"{theme.get('wcag_pass')}"
                    )


                    # ======================================
                    # Viewport Loop
                    # ======================================

                    for viewport in viewports:

                        print(
                            "Rendering: "
                            f"{selected_section}"
                            f" | "
                            f"{theme_mode}"
                            f" | "
                            f"{viewport['name']}"
                            f" "
                            f"("
                            f"{viewport['width']}"
                            f"x"
                            f"{viewport['height']}"
                            f")"
                        )


                        await render_page(

                            # ==============================
                            # Browser
                            # ==============================

                            browser=
                                browser,


                            # ==============================
                            # Sample
                            # ==============================

                            sample_index=
                                sample_index,

                            page_type=
                                "settings",


                            # ==============================
                            # Template
                            # ==============================

                            template_name=
                                "pages/settings.html",

                            context_key=
                                "page",

                            page_data=
                                settings_page,


                            # ==============================
                            # System
                            # ==============================

                            system=
                                None,


                            # ==============================
                            # Theme
                            # ==============================

                            theme=
                                theme,


                            # ==============================
                            # Viewport
                            # ==============================

                            viewport=
                                viewport,


                            # ==============================
                            # Paths
                            # ==============================

                            template_dir=
                                TEMPLATE_DIR,

                            output_root=
                                OUTPUT_ROOT,


                            # ==============================
                            # Output Separation
                            #
                            # Section must be part of the
                            # directory because each section
                            # uses the same page_type and
                            # sample_index.
                            # ==============================

                            output_subdir=(
                                f"settings/"
                                f"{theme_mode}/"
                                f"{selected_section}"
                            ),


                            # ==============================
                            # Scroll
                            # ==============================

                            scroll_percentages=
                                SCROLL_PERCENTAGES,


                            # ==============================
                            # Full Page
                            # ==============================

                            save_full_page=
                                SAVE_FULL_PAGE,


                            # ==============================
                            # Viewport Captures
                            # ==============================

                            save_viewports=
                                SAVE_VIEWPORTS,
                        )


        # ==================================================
        # Close Browser
        # ==================================================

        await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )