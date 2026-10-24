from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from tqdm import tqdm

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.dynamic_system_generator import (
    generate_system_data,
)
from social_media.common.viewport import get_viewports_by_names

from social_media.sephora.generators.product_generator import (
    PRODUCT_STATES,
    apply_product_state,
    generate_product_data,
)
from social_media.sephora.renderers.common_renderer import (
    render_sephora_page,
)


NUM_SAMPLES = 5

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

SELECTED_STATES = list(PRODUCT_STATES)

THEME_MODES = ["light", "dark"]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

MAX_CONCURRENT_WORKERS = 4

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]

SAVE_VISUALIZATIONS = True
MIN_VISIBLE_RATIO = 0.20

MEDIA_DIR: Path | None = None

SYSTEM_STYLE = "random"
SYSTEM_ICON_DENSITY = "random"
SYSTEM_TOP_BAR = None


def generate_themes() -> dict:
    for _ in range(100):
        first = generate_accessible_theme(mode=THEME_MODES[0])
        themes = {THEME_MODES[0]: first}

        try:
            for mode in THEME_MODES[1:]:
                themes[mode] = generate_accessible_theme(
                    seed=first["seed"],
                    mode=mode,
                    max_attempts=1,
                )
            return themes
        except RuntimeError:
            continue

    raise RuntimeError(
        "Unable to generate matching themes for all requested modes."
    )


async def render_job(
    browser,
    semaphore,
    sample_index,
    state,
    data,
    system,
    theme,
    viewport,
):
    metadata = {
        "sample": sample_index,
        "state": state,
        "theme": theme["mode"],
        "viewport": viewport["name"],
    }

    async with semaphore:
        try:
            await render_sephora_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"product_{state}",
                template_name="product.html",
                context_key="sephora",
                page_data=data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="product",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0]
                    if data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                min_visible_ratio=MIN_VISIBLE_RATIO,
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {**metadata, "status": "success"}

        except Exception as error:
            return {
                **metadata,
                "status": "failed",
                "error": repr(error),
            }


async def main(browser):
    if NUM_SAMPLES < 1 or MAX_CONCURRENT_WORKERS < 1:
        raise ValueError("Samples and workers must be positive.")

    if not THEME_MODES or not SELECTED_STATES or not SELECTED_VIEWPORTS:
        raise ValueError("Select themes, states, and viewports.")

    if set(THEME_MODES) - {"light", "dark"}:
        raise ValueError("Unsupported theme mode.")

    if set(SELECTED_STATES) - set(PRODUCT_STATES):
        raise ValueError("Unsupported product state.")

    for values in [
        THEME_MODES,
        SELECTED_STATES,
        SELECTED_VIEWPORTS,
    ]:
        if len(values) != len(set(values)):
            raise ValueError("Duplicate selections cause filename collisions.")

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError("Enable at least one capture mode.")

    if MEDIA_DIR is not None and not Path(MEDIA_DIR).is_dir():
        raise FileNotFoundError(MEDIA_DIR)

    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    total = (
        NUM_SAMPLES
        * len(viewports)
        * len(THEME_MODES)
        * len(SELECTED_STATES)
    )

    failed = []

    with tqdm(total=total, desc="Sephora product", unit="job") as progress:
        for sample_index in range(1, NUM_SAMPLES + 1):
            base = generate_product_data(
                sample_index=sample_index,
                media_dir=MEDIA_DIR,
            )

            themes = generate_themes()

            systems = {
                viewport["name"]: generate_system_data(
                    style=SYSTEM_STYLE,
                    icon_density=SYSTEM_ICON_DENSITY,
                    viewport=viewport,
                    top_bar=SYSTEM_TOP_BAR,
                )
                for viewport in viewports
            }

            states = {
                state: apply_product_state(base, state)
                for state in SELECTED_STATES
            }

            tasks = [
                asyncio.create_task(
                    render_job(
                        browser,
                        semaphore,
                        sample_index,
                        state,
                        states[state],
                        systems[viewport["name"]],
                        themes[mode],
                        viewport,
                    )
                )
                for mode in THEME_MODES
                for viewport in viewports
                for state in SELECTED_STATES
            ]

            try:
                for completed in asyncio.as_completed(tasks):
                    result = await completed
                    progress.update(1)

                    if result["status"] == "failed":
                        failed.append(result)
                        tqdm.write(f"[PRODUCT FAILED] {result}")

            finally:
                for task in tasks:
                    if not task.done():
                        task.cancel()

                await asyncio.gather(*tasks, return_exceptions=True)

    print("Successful jobs:", total - len(failed))
    print("Failed jobs:", len(failed))

    return failed


async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        try:
            failed = await main(browser)
        finally:
            await browser.close()

    if failed:
        raise RuntimeError(f"{len(failed)} product render jobs failed.")


if __name__ == "__main__":
    asyncio.run(run())