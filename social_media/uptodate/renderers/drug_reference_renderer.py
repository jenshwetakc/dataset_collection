from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.dynamic_system_generator import (
    generate_system_data,
)
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.uptodate.generators.drug_reference_generator import (
    DRUG_REFERENCE_STATES,
    apply_drug_reference_state,
    generate_drug_reference_data,
)
from social_media.uptodate.renderers.common_renderer import (
    render_page,
)


UPTODATE_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = UPTODATE_ROOT / "templates"
OUTPUT_ROOT = UPTODATE_ROOT / "output"

NUM_SAMPLES = 8

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

THEME_MODE = "random"

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]

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


async def render_drug_reference_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    page_data: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = page_data["state"]

        try:
            print(
                f"[UPTODATE DRUG REFERENCE] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            system = generate_system_data(
                style="random",
                icon_density="random",
                viewport=viewport,
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"drug_reference_{state}",
                template_name="drug_reference.html",
                context_key="uptodate",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir="drug_reference",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0]
                    if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=True,
            )

            return {
                "status": "success",
                "state": state,
                "viewport": viewport["name"],
                "sample_index": sample_index,
            }

        except Exception as error:
            print(
                f"[UPTODATE DRUG REFERENCE FAILED] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"error={error!r}"
            )

            return {
                "status": "failed",
                "state": state,
                "viewport": viewport["name"],
                "sample_index": sample_index,
                "error": repr(error),
            }


async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    state_order = list(DRUG_REFERENCE_STATES)
    random.shuffle(state_order)

    successful = 0
    failures = []

    for sample_index in range(NUM_SAMPLES):
        state = state_order[
            sample_index % len(state_order)
        ]

        page_data = apply_drug_reference_state(
            generate_drug_reference_data(
                sample_index=sample_index,
            ),
            state,
        )

        theme = generate_theme()

        results = await asyncio.gather(
            *[
                render_drug_reference_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    page_data=page_data,
                    theme=theme,
                    viewport=viewport,
                )
                for viewport in viewports
            ]
        )

        successful += sum(
            result["status"] == "success"
            for result in results
        )

        failures.extend(
            result
            for result in results
            if result["status"] == "failed"
        )

    print(
        f"[UPTODATE DRUG REFERENCE COMPLETE] "
        f"successful={successful} "
        f"failed={len(failures)}"
    )

    if failures:
        raise RuntimeError(
            f"{len(failures)} drug reference jobs failed. "
            "See the job errors above."
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