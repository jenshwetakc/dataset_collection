from __future__ import annotations

import asyncio

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
from social_media.sephora.generators.stores_generator import (
    STORES_STATES,
    apply_stores_state,
    generate_stores_data,
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

SELECTED_STATES = STORES_STATES.copy()

THEME_MODES = [
    "light",
    "dark",
]

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


def validate_configuration() -> None:
    if NUM_SAMPLES < 1:
        raise ValueError("NUM_SAMPLES must be positive.")

    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "MAX_CONCURRENT_WORKERS must be positive."
        )

    for name, values in [
        ("states", SELECTED_STATES),
        ("viewports", SELECTED_VIEWPORTS),
        ("themes", THEME_MODES),
        ("annotation profiles", ANNOTATION_PROFILES),
    ]:
        if not values:
            raise ValueError(
                f"Selected {name} cannot be empty."
            )

        if len(values) != len(set(values)):
            raise ValueError(
                f"Selected {name} contain duplicates."
            )

    unknown_states = (
        set(SELECTED_STATES) - set(STORES_STATES)
    )

    if unknown_states:
        raise ValueError(
            f"Unknown states: {sorted(unknown_states)}"
        )

    if set(THEME_MODES) - {"light", "dark"}:
        raise ValueError(
            "Theme modes must be light or dark."
        )

    if set(ANNOTATION_PROFILES) - {
        "big_components",
        "small_elements",
    }:
        raise ValueError(
            "Unknown annotation profile."
        )

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError(
            "Enable at least one capture mode."
        )

    if not 0 < MIN_VISIBLE_RATIO <= 1:
        raise ValueError(
            "MIN_VISIBLE_RATIO must be in (0, 1]."
        )

    if CAPTURE_VIEWPORTS:
        if not SCROLL_PERCENTAGES:
            raise ValueError(
                "SCROLL_PERCENTAGES cannot be empty."
            )

        if any(
            not 0 <= percentage <= 100
            for percentage in SCROLL_PERCENTAGES
        ):
            raise ValueError(
                "Scroll percentages must be between 0 and 100."
            )


def generate_themes() -> dict:
    """Generate theme modes using a shared seed."""

    last_error = None

    for _ in range(100):
        try:
            first_mode = THEME_MODES[0]

            first_theme = generate_accessible_theme(
                mode=first_mode,
                max_attempts=1,
            )

            seed = first_theme["seed"]

            themes = {
                first_mode: first_theme,
            }

            for mode in THEME_MODES[1:]:
                themes[mode] = generate_accessible_theme(
                    seed=seed,
                    mode=mode,
                    max_attempts=1,
                )

            return themes

        except RuntimeError as error:
            last_error = error

    raise RuntimeError(
        "Could not generate accessible themes "
        "with a shared seed."
    ) from last_error


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
                page_type=f"stores_{page_data['state']}",
                template_name="stores.html",
                context_key="sephora",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="stores",
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


async def main(browser) -> list[dict]:
    validate_configuration()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    total_jobs = (
        NUM_SAMPLES
        * len(SELECTED_STATES)
        * len(THEME_MODES)
        * len(viewports)
    )

    successful = 0
    failed = []

    with tqdm(
        total=total_jobs,
        desc="Sephora Stores",
    ) as progress:

        for sample_index in range(
            1,
            NUM_SAMPLES + 1,
        ):
            base_data = generate_stores_data(
                sample_index=sample_index,
            )

            themes = generate_themes()

            systems = {
                viewport["name"]: generate_system_data(
                    viewport=viewport,
                )
                for viewport in viewports
            }

            states = {
                state: apply_stores_state(
                    base_data,
                    state,
                )
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
                        tqdm.write(
                            f"[STORES FAILED] {result}"
                        )

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
            f"{len(failed)} stores jobs failed."
        )


if __name__ == "__main__":
    asyncio.run(run())