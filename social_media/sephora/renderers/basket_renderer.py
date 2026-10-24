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
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.sephora.generators.basket_generator import (
    BASKET_STATES,
    apply_basket_state,
    generate_basket_data,
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

SELECTED_STATES = BASKET_STATES.copy()

THEME_MODES = ["light", "dark"]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

MAX_CONCURRENT_WORKERS = 4

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SAVE_VISUALIZATIONS = True

SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]

MIN_VISIBLE_RATIO = 0.20

# None uses the shared asset directory.
MEDIA_DIR: Path | None = None


def generate_themes() -> dict:
    for _ in range(100):
        try:
            first_mode = THEME_MODES[0]

            first_theme = generate_accessible_theme(
                mode=first_mode,
            )

            themes = {
                first_mode: first_theme,
            }

            for mode in THEME_MODES[1:]:
                themes[mode] = generate_accessible_theme(
                    seed=first_theme["seed"],
                    mode=mode,
                    max_attempts=1,
                )

            return themes

        except RuntimeError:
            continue

    raise RuntimeError(
        "Could not generate accessible themes for all modes."
    )


async def render_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    page_data: dict,
    system: dict,
    theme: dict,
    theme_mode: str,
    viewport: dict,
) -> dict:

    result = {
        "sample_index": sample_index,
        "state": page_data["state"],
        "theme": theme_mode,
        "viewport": viewport["name"],
    }

    async with semaphore:
        try:
            await render_sephora_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"basket_{page_data['state']}",
                template_name="basket.html",
                context_key="sephora",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="basket",
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=MIN_VISIBLE_RATIO,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0]
                    if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            result["status"] = "success"

        except Exception as error:
            result["status"] = "failed"
            result["error"] = repr(error)

    return result


def validate_configuration() -> None:
    if NUM_SAMPLES < 1 or MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "Sample count and worker count must be positive."
        )

    for name, values in [
        ("viewports", SELECTED_VIEWPORTS),
        ("states", SELECTED_STATES),
        ("themes", THEME_MODES),
    ]:
        if not values:
            raise ValueError(f"No {name} selected.")

        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate {name} selected.")

    unknown_states = set(SELECTED_STATES) - set(BASKET_STATES)

    if unknown_states:
        raise ValueError(
            f"Unknown states: {sorted(unknown_states)}"
        )

    if set(THEME_MODES) - {"light", "dark"}:
        raise ValueError("Theme modes must be light or dark.")

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError("Enable at least one capture mode.")

    if MEDIA_DIR is not None and not Path(MEDIA_DIR).is_dir():
        raise ValueError(f"Missing media directory: {MEDIA_DIR}")


async def main(browser) -> list[dict]:
    validate_configuration()

    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    total = (
        NUM_SAMPLES
        * len(SELECTED_STATES)
        * len(THEME_MODES)
        * len(viewports)
    )

    failed = []
    successful = 0

    with tqdm(total=total, desc="Sephora Basket") as progress:
        for sample_index in range(1, NUM_SAMPLES + 1):
            base_data = generate_basket_data(
                sample_index=sample_index,
                media_dir=MEDIA_DIR,
            )

            themes = generate_themes()

            systems = {
                viewport["name"]: generate_system_data(
                    viewport=viewport,
                )
                for viewport in viewports
            }

            states = {
                state: apply_basket_state(base_data, state)
                for state in SELECTED_STATES
            }

            tasks = [
                asyncio.create_task(
                    render_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        page_data=states[state],
                        system=systems[viewport["name"]],
                        theme=themes[mode],
                        theme_mode=mode,
                        viewport=viewport,
                    )
                )
                for mode in THEME_MODES
                for viewport in viewports
                for state in SELECTED_STATES
            ]

            try:
                for task in asyncio.as_completed(tasks):
                    result = await task

                    if result["status"] == "success":
                        successful += 1
                    else:
                        failed.append(result)
                        tqdm.write(f"[BASKET FAILED] {result}")

                    progress.update(1)

            finally:
                for task in tasks:
                    if not task.done():
                        task.cancel()

                await asyncio.gather(
                    *tasks,
                    return_exceptions=True,
                )

    print(f"Successful jobs: {successful}")
    print(f"Failed jobs: {len(failed)}")

    return failed


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            failed = await main(browser)
        finally:
            await browser.close()

    if failed:
        raise RuntimeError(
            f"{len(failed)} basket rendering jobs failed."
        )


if __name__ == "__main__":
    asyncio.run(run())