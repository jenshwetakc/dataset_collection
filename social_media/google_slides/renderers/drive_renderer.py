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

from social_media.google_slides.generators.drive_generator import (
    generate_drive_data,
)

from social_media.google_slides.renderers.common_renderer import (
    render_google_slides_page,
)


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


def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode,
    )


async def render_drive_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    drive: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[GOOGLE DRIVE] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']} "
                f"state={drive['state']}"
            )

            await render_google_slides_page(
                browser=browser,
                sample_index=sample_index,
                page_type="google_drive",
                template_name="drive.html",
                context_key="page_data",
                page_data=drive,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="google_drive",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[GOOGLE DRIVE FAILED] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    for sample_index in range(NUM_SAMPLES):
        drive = generate_drive_data()
        system = generate_system_data()
        theme = generate_theme()

        print(
            f"\n[GOOGLE DRIVE SAMPLE {sample_index}] "
            f"state={drive['state']} "
            f"theme={theme['mode']}"
        )

        for viewport in viewports:
            jobs.append(
                render_drive_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    drive=drive,
                    system=system,
                    theme=theme,
                    viewport=viewport,
                )
            )

    results = await asyncio.gather(*jobs)

    successful = sum(
        result["status"] == "success"
        for result in results
    )

    print(
        f"[GOOGLE DRIVE COMPLETE] "
        f"successful={successful} "
        f"failed={len(results) - successful}"
    )


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