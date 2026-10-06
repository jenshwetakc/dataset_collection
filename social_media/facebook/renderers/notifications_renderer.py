from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.system_generator import (
    generate_system_data,
)
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.facebook.generators.notifications_generator import (
    generate_notifications_data,
)
from social_media.facebook.renderers.common_renderer import (
    render_facebook_page,
)

# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 20

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
# Theme
# ==========================================================

def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )
    return generate_accessible_theme(mode=mode)


# ==========================================================
# Render Job
# ==========================================================

async def render_notifications_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    notifications_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                "[FACEBOOK NOTIFICATIONS]",
                "sample=",
                sample_index,
                "viewport=",
                # viewport["namename"],
                "theme=",
                theme["mode"],
                "state=",
            )

            await render_facebook_page(
                browser=browser,
                sample_index=sample_index,
                page_type="notifications",
                template_name="notifications.html",
                context_key="notifications",
                page_data=notifications_data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="notifications",
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
                "[FACEBOOK NOTIFICATIONS FAILED]",
                "sample=",
                sample_index,
                "viewport=",
                viewport["name"],
                "error=",
                error,
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )
    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )
    jobs = []

    for sample_index in range(NUM_SAMPLES):
        notifications_data = generate_notifications_data()
        system = generate_system_data()
        theme = generate_theme()

        print(
            "[FACEBOOK NOTIFICATIONS SAMPLE]",
            "sample=",
            sample_index,
            "theme=",
            theme["mode"],
            "state=",
            notifications_data["state"]["name"],
            "notifications=",
            len(notifications_data["notifications"]),
        )

        for viewport in viewports:
            jobs.append(
                render_notifications_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    notifications_data=notifications_data,
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
    failed = len(results) - successful

    print(
        "[FACEBOOK NOTIFICATIONS COMPLETE]",
        "successful=",
        successful,
        "failed=",
        failed,
    )


# ==========================================================
# Entry Point
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True
        )

        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())