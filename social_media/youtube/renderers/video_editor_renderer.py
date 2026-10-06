from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import (
    async_playwright,
)
from tqdm import tqdm

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.youtube.generators.video_editor_generator import (
    EDITOR_STATES,
    generate_video_editor_page,
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
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 5
MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Editor States
# ==========================================================

EDITOR_STATES_TO_RENDER = [
    "idle",
    "playing",
    "trim_start_selected",
    "trim_end_selected",
    "playhead_middle",
]


# ==========================================================
# Theme Configuration
# ==========================================================

THEME_MODES = [
    "light",
    "dark",
]


# ==========================================================
# Viewport Configuration
# ==========================================================

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


# ==========================================================
# Scroll and Capture Configuration
# ==========================================================

SCROLL_PERCENTAGES = [
    0,
]

SAVE_FULL_PAGE = False
SAVE_VIEWPORTS = True


def validate_editor_states() -> None:
    unknown_states = [
        state
        for state in EDITOR_STATES_TO_RENDER
        if state not in EDITOR_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown editor states: "
            f"{unknown_states}. "
            f"Available states: {EDITOR_STATES}"
        )


async def render_video_editor_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    editor_state: str,
    editor_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE VIDEO EDITOR] "
                f"sample={sample_index} "
                f"state={editor_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"video_editor{editor_state}",
                template_name="pages/video_editor.html",
                context_key="page",
                page_data=editor_page,
                system=None,
                theme=theme,
                viewport=viewport,

                output_subdir="video_editor",
                # (
                #     f"video_editor/"
                #     f"{theme_mode}/"
                #     f"{editor_state}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": editor_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE VIDEO EDITOR FAILED] "
                f"sample={sample_index} "
                f"state={editor_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": editor_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_editor_states()

    viewports = get_viewports_by_names(
       SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE VIDEO EDITOR")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Editor states: {EDITOR_STATES_TO_RENDER}")
    print(f"Themes: {THEME_MODES}")
    print(f"Save full page: {SAVE_FULL_PAGE}")
    print(f"Save viewport: {SAVE_VIEWPORTS}")
    print(f"Scroll positions: {SCROLL_PERCENTAGES}")
    print("\nTesting viewports:")

    for viewport in viewports:
        orientation = (
            "landscape"
            if viewport["width"] > viewport["height"]
            else "portrait"
        )

        print(
            f"  - {viewport['name']} | "
            f"{viewport['width']}x{viewport['height']} | "
            f"{orientation} | "
            f"DPR={viewport.get('dpr', 1)}"
        )

    for sample_index in tqdm(
        range(NUM_SAMPLES),
        desc="YouTube Video Editor",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for editor_state in EDITOR_STATES_TO_RENDER:
            editor_page = generate_video_editor_page(
                state=editor_state,
            )

            print("\n======================================")
            print(f"Editor state: {editor_state}")
            print(f"Video: {editor_page['video']['title']}")
            print(f"Duration: {editor_page['video']['duration_text']}")
            print(
                "Trim: "
                f"{editor_page['trim']['start_text']} -> "
                f"{editor_page['trim']['end_text']}"
            )
            print(
                "Selected duration: "
                f"{editor_page['trim']['selected_duration_text']}"
            )
            print(
                "Playhead: "
                f"{editor_page['playhead']['current_time_text']}"
            )
            print(f"Playing: {editor_page['playback']['playing']}")
            print(
                "Start selected: "
                f"{editor_page['handles']['start_selected']}"
            )
            print(
                "End selected: "
                f"{editor_page['handles']['end_selected']}"
            )

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_video_editor_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            editor_state=editor_state,
                            editor_page=editor_page,
                            theme_mode=theme_mode,
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
        f"[YOUTUBE VIDEO EDITOR COMPLETE] "
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