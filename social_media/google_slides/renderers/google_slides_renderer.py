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

from social_media.google_slides.generators.slides_generator import (
    generate_google_slides_data,
)

from social_media.google_slides.renderers.common_renderer import (
    render_google_slides_page,
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 25


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
    # "ultrawide",
]


ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


THEME_MODE = "random"


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
# Theme Helper
# ==========================================================

def generate_theme() -> dict:
    mode = (
        random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode,
    )


# ==========================================================
# Render One Job
# ==========================================================

async def render_google_slides_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    google_slides: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[GOOGLE SLIDES] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']} "
                f"state={google_slides['state']}"
            )

            await render_google_slides_page(
                browser=browser,
                sample_index=sample_index,
                page_type="google_slides",
                template_name="slides.html",
                context_key="page_data",
                page_data=google_slides,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="google_slides",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "state": google_slides["state"],
            }

        except Exception as error:
            print(
                f"[GOOGLE SLIDES FAILED] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "state": google_slides["state"],
                "error": str(error),
            }


# ==========================================================
# Main Generation Loop
# ==========================================================

async def main(
    browser,
) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    for sample_index in range(NUM_SAMPLES):
        google_slides = (
            generate_google_slides_data()
        )

        system = generate_system_data()

        theme = generate_theme()

        print(
            "\n=========================================="
        )

        print(
            "GOOGLE SLIDES SAMPLE",
            sample_index,
        )

        print(
            "State:",
            google_slides["state"],
        )

        print(
            "Presentation:",
            google_slides["presentation"]["title"],
        )

        print(
            "Selected slide:",
            google_slides["selected_slide_number"],
        )

        print(
            "Theme:",
            theme["mode"],
        )

        print(
            "=========================================="
        )

        for viewport in viewports:
            jobs.append(
                render_google_slides_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    google_slides=google_slides,
                    system=system,
                    theme=theme,
                    viewport=viewport,
                )
            )

    results = await asyncio.gather(
        *jobs
    )

    successful = sum(
        result["status"] == "success"
        for result in results
    )

    failed = len(results) - successful

    print(
        f"[GOOGLE SLIDES COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
    )


# ==========================================================
# Browser Entry Point
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            await main(browser)

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())