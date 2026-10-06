from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import (
    async_playwright,
)
from tqdm import tqdm

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.youtube.generators.home_generator import (
    generate_home_page,
)
from social_media.youtube.renderers.common_new import (
   render_youtube_page
)
from social_media.common.viewport import (
    get_viewports_by_names,
)


# ==========================================================
# Paths
# ==========================================================

YOUTUBE_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = YOUTUBE_ROOT / "templates"
OUTPUT_ROOT = YOUTUBE_ROOT / "output"


# ==========================================================
# Config
# ==========================================================

NUM_SAMPLES = 5
MAX_CONCURRENT_WORKERS = 4

VIEWPORT_MODE = "selected"

SELECTED_VIEWPORTS = [
    "small_mobile",
    # "standard_android",
    # "standard_iphone",
    # "large_mobile",
    # "mobile_landscape",
    # "tablet_portrait",
    # "large_tablet_portrait",
    # "tablet_landscape",
    # "foldable",
    # "small_laptop",
    # "laptop",
    # "large_laptop",
    # "desktop_fhd",
    # "desktop_qhd",
    # "desktop_4k",
    "ultrawide",
]


ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

SAVE_FULL_PAGE = False
SAVE_VIEWPORTS = True


async def render_home_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    home: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE HOME] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type="home",
                template_name="pages/home.html",
                context_key="page",
                page_data=home,
                system=None,
                theme=theme,
                viewport=viewport,
                output_subdir="home",
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE HOME FAILED] "
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
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==============================")
    print("YOUTUBE HOME DATASET")
    print("==============================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Full page capture: {SAVE_FULL_PAGE}")
    print(f"Viewport capture: {SAVE_VIEWPORTS}")
    print(f"Scroll positions: {SCROLL_PERCENTAGES}")
    print("\nViewports:")

    for viewport in viewports:
        print(
            f"  - {viewport['name']} "
            f"({viewport['width']}x{viewport['height']}, "
            f"DPR={viewport.get('dpr', 1)})"
        )

    for sample_index in tqdm(
        range(NUM_SAMPLES),
        desc="YouTube Home",
    ):
        home = generate_home_page()

        theme_mode = random.choice(["light", "dark"])
        theme = generate_accessible_theme(mode=theme_mode)

        print(
            f"[YOUTUBE HOME SAMPLE] "
            f"sample={sample_index} "
            f"theme={theme_mode}"
        )

        for viewport in viewports:
            jobs.append(
                render_home_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    home=home,
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
        f"[YOUTUBE HOME COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
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