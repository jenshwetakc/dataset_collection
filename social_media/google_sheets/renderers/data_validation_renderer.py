from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.google_sheets.generators.data_validation_generator import (
    DATA_VALIDATION_STATES,
    generate_data_validation_data,
)
from social_media.google_sheets.renderers.common_renderer import render_google_sheets_page


NUM_SAMPLES_PER_STATE = 25
SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_android", "standard_iphone", "large_mobile",
    "mobile_landscape", "tablet_portrait", "large_tablet_portrait",
    "tablet_landscape", "foldable", "small_laptop", "laptop",
    "large_laptop", "desktop_fhd", "desktop_qhd", "desktop_4k",
    "ultrawide",
]
ANNOTATION_PROFILES = ["big_components", "small_elements"]
THEME_MODE = "random"
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
SAVE_VISUALIZATIONS = True
MAX_CONCURRENT_WORKERS = 4


def generate_theme() -> dict:
    mode = random.choice(["light", "dark"]) if THEME_MODE == "random" else THEME_MODE
    if mode not in {"light", "dark"}:
        raise ValueError("THEME_MODE must be 'light', 'dark', or 'random'.")
    return generate_accessible_theme(mode=mode)


async def render_data_validation_job(
    *, browser, semaphore: asyncio.Semaphore, state: str,
    sample_index: int, viewport: dict, seed: int,
) -> dict:
    async with semaphore:
        try:
            theme = generate_theme()
            validation = generate_data_validation_data(
                state=state, viewport=viewport, seed=seed,
            )
            print(
                f"[SHEETS DATA VALIDATION] state={state} sample={sample_index} "
                f"viewport={viewport['name']} theme={theme['mode']}"
            )
            await render_google_sheets_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"data_validation_{state}",
                template_name="data_validation.html",
                context_key="validation",
                page_data=validation,
                system=generate_system_data(),
                theme=theme,
                viewport=viewport,
                output_subdir="data_validation",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
                save_visualizations=SAVE_VISUALIZATIONS,
            )
            return {"status": "success", "state": state, "viewport": viewport["name"]}
        except Exception as error:
            print(
                f"[SHEETS DATA VALIDATION FAILED] state={state} sample={sample_index} "
                f"viewport={viewport['name']} error={error!r}"
            )
            return {"status": "failed", "state": state, "viewport": viewport["name"], "error": str(error)}


async def main(browser) -> None:
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []
    seed = 0
    for state in DATA_VALIDATION_STATES:
        for sample_index in range(NUM_SAMPLES_PER_STATE):
            for viewport in viewports:
                jobs.append(render_data_validation_job(
                    browser=browser, semaphore=semaphore, state=state,
                    sample_index=sample_index, viewport=viewport, seed=seed,
                ))
                seed += 1
    results = await asyncio.gather(*jobs)
    successful = sum(result["status"] == "success" for result in results)
    print(f"[SHEETS DATA VALIDATION COMPLETE] successful={successful} failed={len(results) - successful}")


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
