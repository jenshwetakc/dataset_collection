from __future__ import annotations

import asyncio

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.renderer import (
    resolve_viewports,
)
from social_media.spotify.generators.settings_generator import (
    generate_settings_page,
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

NUM_SAMPLES = 20

VIEWPORT_MODE = "selected"

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
    "small_elements",
]

THEME_MODES = [
    "light",
    "dark",
]

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Render One Parallel Settings Job
# ==========================================================

async def render_one_settings_job(
    browser,
    semaphore,
    sample_index: int,
    settings_data: dict,
    system: dict,
    theme: dict,
    theme_mode: str,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                "\n"
                "=========================================="
            )

            print("SPOTIFY SETTINGS")
            print("Sample:", sample_index)
            print("Theme:", theme_mode)
            print(
                "Account plan:",
                settings_data["account"]["plan"],
            )
            print(
                "Storage:",
                f"{settings_data['storage']['used']}/"
                f"{settings_data['storage']['total']} GB",
            )
            print("Viewport:", viewport["name"])

            print(
                "=========================================="
            )

            await render_spotify_page(

                browser=browser,

                sample_index=sample_index,

                page_type="settings",

                template_name="settings.html",

                context_key="settings",

                page_data=settings_data,

                system=system,

                theme=theme,

                viewport=viewport,

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:

            return {
                "status": "failed",
                "sample_index": sample_index,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main Generation
# ==========================================================

async def main(
    browser,
) -> None:

    viewports = resolve_viewports(

        mode=VIEWPORT_MODE,

        selected=SELECTED_VIEWPORTS,
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    print(
        "Spotify Settings Dataset Generation | "
        f"jobs={NUM_SAMPLES * len(THEME_MODES) * len(viewports)} | "
        f"workers={MAX_CONCURRENT_WORKERS}"
    )

    for sample_index in range(
        1,
        NUM_SAMPLES + 1,
    ):

        settings_data = generate_settings_page()

        system = generate_system_data()

        for theme_mode in THEME_MODES:

            theme = generate_accessible_theme(
                mode=theme_mode
            )

            for viewport in viewports:

                jobs.append(

                    render_one_settings_job(

                        browser=browser,

                        semaphore=semaphore,

                        sample_index=sample_index,

                        settings_data=settings_data,

                        system=system,

                        theme=theme,

                        theme_mode=theme_mode,

                        viewport=viewport,
                    )
                )

    results = await asyncio.gather(
        *jobs
    )

    successful_results = [
        result
        for result in results
        if result["status"] == "success"
    ]

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    print(
        "Generation complete | "
        f"successful={len(successful_results)} | "
        f"failed={len(failed_results)}"
    )

    for result in failed_results:

        print(
            "[FAILED]",
            "Sample:", result["sample_index"],
            "| Theme:", result["theme"],
            "| Viewport:", result["viewport"],
            "| Error:", result["error"],
        )


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run() -> None:

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        try:

            await main(
                browser
            )

        finally:

            await browser.close()


## ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )