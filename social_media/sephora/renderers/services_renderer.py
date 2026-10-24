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

from social_media.sephora.generators.services_generator import (
    SERVICES_STATES,
    apply_services_state,
    generate_services_data,
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

SELECTED_STATES = SERVICES_STATES.copy()

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

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MIN_VISIBLE_RATIO = 0.20

# None uses the shared media directory.
# Alternatively:
# MEDIA_DIR = Path("/absolute/path/to/assets/sephora")
MEDIA_DIR: Path | None = None

SYSTEM_STYLE = None
SYSTEM_ICON_DENSITY = "random"


# ==========================================================
# Validate Configuration
# ==========================================================

def validate_configuration() -> None:
    if NUM_SAMPLES < 1:
        raise ValueError("NUM_SAMPLES must be positive.")

    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError(
            "MAX_CONCURRENT_WORKERS must be positive."
        )

    for name, values in [
        ("SELECTED_VIEWPORTS", SELECTED_VIEWPORTS),
        ("SELECTED_STATES", SELECTED_STATES),
        ("THEME_MODES", THEME_MODES),
        ("ANNOTATION_PROFILES", ANNOTATION_PROFILES),
    ]:
        if not values:
            raise ValueError(f"{name} cannot be empty.")

        if len(values) != len(set(values)):
            raise ValueError(
                f"{name} contains duplicate values."
            )

    unknown_states = (
        set(SELECTED_STATES)
        - set(SERVICES_STATES)
    )

    if unknown_states:
        raise ValueError(
            f"Unknown service states: {sorted(unknown_states)}"
        )

    unknown_modes = (
        set(THEME_MODES)
        - {"light", "dark"}
    )

    if unknown_modes:
        raise ValueError(
            f"Unknown theme modes: {sorted(unknown_modes)}"
        )

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError(
            "Enable CAPTURE_FULL_PAGE or CAPTURE_VIEWPORTS."
        )

    if not 0 <= MIN_VISIBLE_RATIO <= 1:
        raise ValueError(
            "MIN_VISIBLE_RATIO must be between 0 and 1."
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

    if MEDIA_DIR is not None:
        if not Path(MEDIA_DIR).is_dir():
            raise ValueError(
                f"Media directory does not exist: {MEDIA_DIR}"
            )


# ==========================================================
# Generate Matching Accessible Themes
# ==========================================================

def generate_themes() -> dict:
    """
    Generate the selected modes using the same palette seed.
    Retry with a new seed if any mode cannot pass validation.
    """
    for _ in range(100):
        try:
            first_mode = THEME_MODES[0]

            first_theme = generate_accessible_theme(
                mode=first_mode,
            )

            themes = {
                first_mode: first_theme,
            }

            for theme_mode in THEME_MODES[1:]:
                themes[theme_mode] = generate_accessible_theme(
                    seed=first_theme["seed"],
                    mode=theme_mode,
                    max_attempts=1,
                )

            return themes

        except RuntimeError:
            continue

    raise RuntimeError(
        "Could not generate accessible themes "
        "for all selected modes."
    )


# ==========================================================
# Render One Job
# ==========================================================

async def render_one_services_job(
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

                # State appears in output filenames.
                page_type=f"services_{page_data['state']}",

                template_name="services.html",
                context_key="sephora",
                page_data=page_data,

                system=system,
                theme=theme,
                viewport=viewport,

                # All service states share this output directory.
                output_subdir="services",

                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=MIN_VISIBLE_RATIO,

                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,

                # Fixed dialogs only need the initial viewport.
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


# ==========================================================
# Render One Sample Across States, Themes, and Viewports
# ==========================================================

async def render_sample(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    viewports: list[dict],
    progress,
) -> list[dict]:

    # Share the same synthetic content across every viewport.
    base_data = generate_services_data(
        sample_index=sample_index,
        media_dir=MEDIA_DIR,
    )

    themes = generate_themes()

    # Each viewport gets its own compatible system configuration.
    systems = {
        viewport["name"]: generate_system_data(
            style=SYSTEM_STYLE,
            icon_density=SYSTEM_ICON_DENSITY,
            viewport=viewport,
        )
        for viewport in viewports
    }

    state_data = {
        state: apply_services_state(
            base_data,
            state,
        )
        for state in SELECTED_STATES
    }

    tasks = [
        asyncio.create_task(
            render_one_services_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                page_data=state_data[state],
                system=systems[viewport["name"]],
                theme=themes[theme_mode],
                theme_mode=theme_mode,
                viewport=viewport,
            )
        )
        for theme_mode in THEME_MODES
        for viewport in viewports
        for state in SELECTED_STATES
    ]

    results = []

    try:
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

            if result["status"] == "failed":
                tqdm.write(
                    "[SERVICES FAILED] "
                    f"sample={result['sample_index']} "
                    f"state={result['state']} "
                    f"theme={result['theme']} "
                    f"viewport={result['viewport']} "
                    f"error={result['error']}"
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

    total_jobs = (
        NUM_SAMPLES
        * len(SELECTED_STATES)
        * len(THEME_MODES)
        * len(viewports)
    )

    print("Sephora Services Dataset Generation")
    print("Samples:", NUM_SAMPLES)
    print("States:", len(SELECTED_STATES))
    print("Themes:", len(THEME_MODES))
    print("Viewports:", len(viewports))
    print("Total jobs:", total_jobs)
    print("Parallel workers:", MAX_CONCURRENT_WORKERS)

    successful_count = 0
    failed_results = []

    with tqdm(
        total=total_jobs,
        desc="Sephora Services",
        unit="job",
    ) as progress:

        # Process one sample at a time to limit image-data memory.
        # Jobs within each sample run concurrently.
        for sample_index in range(
            1,
            NUM_SAMPLES + 1,
        ):
            results = await render_sample(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                viewports=viewports,
                progress=progress,
            )

            successful_count += sum(
                result["status"] == "success"
                for result in results
            )

            failed_results.extend(
                result
                for result in results
                if result["status"] == "failed"
            )

    print("Generation complete")
    print("Successful jobs:", successful_count)
    print("Failed jobs:", len(failed_results))

    return failed_results


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            failed_results = await main(browser)

        finally:
            await browser.close()

    if failed_results:
        raise RuntimeError(
            f"{len(failed_results)} service rendering jobs failed. "
            "See the failure messages above."
        )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    asyncio.run(run())