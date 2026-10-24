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

from social_media.sephora.generators.skincare_generator import (
    SKINCARE_STATES,
    apply_skincare_state,
    generate_skincare_data,
)

from social_media.sephora.renderers.common_renderer import (
    render_sephora_page,
)


# ==========================================================
# Dataset Configuration
# ==========================================================

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

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODES = [
    "light",
    "dark",
]

SELECTED_STATES = [
    "browse",
    "filtered",
    "sort_open",
    "filter_open",
    "quicklook",
    "empty_results",
]

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

MIN_VISIBLE_RATIO = 0.20
SAVE_VISUALIZATIONS = True

SYSTEM_STYLE = "random"
SYSTEM_ICON_DENSITY = "random"

# None uses the platform's default placement.
# True places every platform bar at the top.
SYSTEM_TOP_BAR = None

# None uses the shared ASSETS_ROOT.
MEDIA_DIR: Path | None = None

# Optional application-specific assets:
# MEDIA_DIR = Path("/absolute/path/to/assets/sephora/skincare")


# ==========================================================
# Configuration Validation
# ==========================================================

def validate_configuration() -> None:
    if NUM_SAMPLES < 1:
        raise ValueError(
            "NUM_SAMPLES must be at least 1."
        )

    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "MAX_CONCURRENT_WORKERS must be at least 1."
        )

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError(
            "Enable CAPTURE_FULL_PAGE or CAPTURE_VIEWPORTS."
        )

    if not 0 <= MIN_VISIBLE_RATIO <= 1:
        raise ValueError(
            "MIN_VISIBLE_RATIO must be between 0 and 1."
        )

    selections = {
        "SELECTED_VIEWPORTS": SELECTED_VIEWPORTS,
        "SELECTED_STATES": SELECTED_STATES,
        "THEME_MODES": THEME_MODES,
        "ANNOTATION_PROFILES": ANNOTATION_PROFILES,
    }

    for name, values in selections.items():
        if not values:
            raise ValueError(
                f"{name} must not be empty."
            )

        if len(values) != len(set(values)):
            raise ValueError(
                f"{name} contains duplicate entries."
            )

    unknown_states = (
        set(SELECTED_STATES)
        - set(SKINCARE_STATES)
    )

    if unknown_states:
        raise ValueError(
            f"Unknown skincare states: "
            f"{sorted(unknown_states)}"
        )

    unknown_modes = (
        set(THEME_MODES)
        - {"light", "dark"}
    )

    if unknown_modes:
        raise ValueError(
            f"Unknown theme modes: "
            f"{sorted(unknown_modes)}"
        )

    if CAPTURE_VIEWPORTS and not SCROLL_PERCENTAGES:
        raise ValueError(
            "SCROLL_PERCENTAGES must not be empty "
            "when viewport capture is enabled."
        )

    if MEDIA_DIR is not None:
        if not Path(MEDIA_DIR).is_dir():
            raise FileNotFoundError(
                f"Media directory does not exist: "
                f"{MEDIA_DIR}"
            )


# ==========================================================
# Generate Matching Light / Dark Themes
# ==========================================================

def generate_sample_themes() -> dict:
    """
    Use the same seed across the requested theme modes.

    A seed must pass the shared palette generator's
    configured checks in every requested mode.
    """

    last_error = None

    for _ in range(100):
        first_mode = THEME_MODES[0]

        first_theme = generate_accessible_theme(
            mode=first_mode,
        )

        seed = first_theme["seed"]

        themes = {
            first_mode: first_theme,
        }

        try:
            for mode in THEME_MODES[1:]:
                themes[mode] = generate_accessible_theme(
                    seed=seed,
                    mode=mode,

                    # A fixed seed/mode is deterministic;
                    # repeating it does not change its result.
                    max_attempts=1,
                )

            return themes

        except RuntimeError as error:
            last_error = error

    raise RuntimeError(
        "Unable to find a shared seed that passes "
        "the configured checks in every requested theme."
    ) from last_error


# ==========================================================
# Render One Parallel Job
# ==========================================================

async def render_one_skincare_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    state: str,
    page_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    metadata = {
        "sample_index": sample_index,
        "state": state,
        "theme": theme["mode"],
        "viewport": viewport["name"],
        "system_style": system["style"],
    }

    async with semaphore:
        try:
            await render_sephora_page(
                browser=browser,
                sample_index=sample_index,

                # Prevent filename collisions between states.
                page_type=f"skincare_{state}",

                template_name="skincare.html",
                context_key="sephora",
                page_data=page_data,
                system=system,
                theme=theme,
                viewport=viewport,

                # All states share the skincare output folder.
                output_subdir="skincare",

                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,

                # The popup remains fixed in the viewport.
                # Window scrolling would repeat that popup.
                scroll_percentages=(
                    [0]
                    if page_data["popup_visible"]
                    else SCROLL_PERCENTAGES
                ),

                min_visible_ratio=MIN_VISIBLE_RATIO,
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                **metadata,
                "status": "success",
            }

        except Exception as error:
            return {
                **metadata,
                "status": "failed",
                "error": repr(error),
            }


# ==========================================================
# Render One Sample
# ==========================================================

async def render_sample(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    viewports: list[dict],
    progress,
) -> list[dict]:
    # Generate one product variation per sample.
    base_data = generate_skincare_data(
        sample_index=sample_index,
        media_dir=MEDIA_DIR,
    )

    themes = generate_sample_themes()

    # Generate platform chrome once per viewport.
    # Reuse it across this sample's themes and states.
    systems = {
        viewport["name"]: generate_system_data(
            style=SYSTEM_STYLE,
            icon_density=SYSTEM_ICON_DENSITY,
            viewport=viewport,
            top_bar=SYSTEM_TOP_BAR,
        )
        for viewport in viewports
    }

    state_data = {
        state: apply_skincare_state(
            base_data,
            state,
        )
        for state in SELECTED_STATES
    }

    tasks = [
        asyncio.create_task(
            render_one_skincare_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                state=state,
                page_data=state_data[state],
                system=systems[viewport["name"]],
                theme=themes[theme_mode],
                viewport=viewport,
            )
        )
        for theme_mode in THEME_MODES
        for viewport in viewports
        for state in SELECTED_STATES
    ]

    results = []

    try:
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            results.append(result)

            progress.update(1)

            if result["status"] == "failed":
                tqdm.write(
                    "[SEPHORA SKINCARE FAILED] "
                    f"sample={result['sample_index']} "
                    f"state={result['state']} "
                    f"theme={result['theme']} "
                    f"viewport={result['viewport']} "
                    f"system={result['system_style']} "
                    f"error={result['error']}"
                )

    finally:
        # Clean up unfinished tasks if the sample is interrupted.
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

    return results


# ==========================================================
# Main Generation
# ==========================================================

async def main(browser) -> list[dict]:
    validate_configuration()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs_per_sample = (
        len(THEME_MODES)
        * len(viewports)
        * len(SELECTED_STATES)
    )

    total_jobs = (
        NUM_SAMPLES
        * jobs_per_sample
    )

    print("Sephora Skincare Dataset Generation")
    print("Samples:", NUM_SAMPLES)
    print("Themes:", len(THEME_MODES))
    print("Viewports:", len(viewports))
    print("States:", len(SELECTED_STATES))
    print("Total jobs:", total_jobs)
    print("Parallel workers:", MAX_CONCURRENT_WORKERS)
    print("Save visualizations:", SAVE_VISUALIZATIONS)

    results = []

    with tqdm(
        total=total_jobs,
        desc="Sephora skincare",
        unit="job",
    ) as progress:
        for sample_index in range(
            1,
            NUM_SAMPLES + 1,
        ):
            # Finish each sample before generating the next.
            # This limits retained base64 image data.
            sample_results = await render_sample(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                viewports=viewports,
                progress=progress,
            )

            results.extend(sample_results)

            successful = sum(
                result["status"] == "success"
                for result in sample_results
            )

            failed = (
                len(sample_results)
                - successful
            )

            tqdm.write(
                "[SEPHORA SAMPLE COMPLETE] "
                f"sample={sample_index} "
                f"successful={successful} "
                f"failed={failed}"
            )

    successful_count = sum(
        result["status"] == "success"
        for result in results
    )

    failed_count = (
        len(results)
        - successful_count
    )

    print("\nGeneration complete")
    print("Successful jobs:", successful_count)
    print("Failed jobs:", failed_count)

    return results


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            results = await main(browser)

        finally:
            await browser.close()

    failed_count = sum(
        result["status"] == "failed"
        for result in results
    )

    if failed_count:
        raise RuntimeError(
            f"{failed_count} Sephora skincare jobs failed. "
            "See the failure messages above."
        )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    asyncio.run(run())