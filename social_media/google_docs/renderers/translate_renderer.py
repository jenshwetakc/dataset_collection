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
from social_media.google_docs.generators.translate_generator import (
    TRANSLATE_STATES,
    generate_translate_data,
)
from social_media.google_docs.renderers.common_renderer import (
    render_google_docs_page,
)


NUM_SAMPLES_PER_STATE = 25

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
SCROLL_PERCENTAGES = [0]

MAX_CONCURRENT_WORKERS = 4
SAVE_VISUALIZATIONS = True


def generate_theme() -> dict:
    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode,
    )


async def render_translate_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    translate: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            await render_google_docs_page(
                browser=browser,
                sample_index=sample_index,
                page_type=(
                    f"translate_{translate['state']}"
                ),
                template_name="translate.html",
                context_key="translate",
                page_data=translate,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="translate",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                "status": "success",
                "state": translate["state"],
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[GOOGLE TRANSLATE FAILED] "
                f"state={translate['state']} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "state": translate["state"],
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS,
    )

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )

    jobs = []

    for state in TRANSLATE_STATES:
        for sample_index in range(
            NUM_SAMPLES_PER_STATE,
        ):
            translate = generate_translate_data(
                state=state,
            )

            system_data = generate_system_data()
            theme = generate_theme()

            for viewport in viewports:
                jobs.append(
                    render_translate_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        translate=translate,
                        system=system_data,
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
        f"[GOOGLE TRANSLATE COMPLETE] "
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