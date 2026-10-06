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
from social_media.youtube.generators.shorts_camera_generator import (
    SHORTS_CAMERA_STATES,
    generate_shorts_camera_page,
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
# Camera States
# ==========================================================

CAMERA_STATES_TO_RENDER = [
    "idle",
    "recording",
    "paused",
    "countdown",
    "recorded",
    "effects_open",
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


def validate_camera_states() -> None:
    unknown_states = [
        state
        for state in CAMERA_STATES_TO_RENDER
        if state not in SHORTS_CAMERA_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown Shorts camera states: "
            f"{unknown_states}. "
            f"Available states: {SHORTS_CAMERA_STATES}"
        )


def print_page_debug(page: dict) -> None:
    print(f"State: {page['state']}")
    print(f"Camera: {page['preview']['camera']}")
    print(f"Flash: {page['preview']['flash']}")
    print(f"Maximum duration: {page['duration']['max_text']}")
    print(f"Recording: {page['recording']['is_recording']}")
    print(f"Paused: {page['recording']['is_paused']}")
    print(f"Has recording: {page['recording']['has_recording']}")
    print(f"Segments: {len(page['segments']['segments'])}")
    print(f"Recorded percent: {page['segments']['recorded_percent']}%")
    print(f"Countdown: {page['countdown']['enabled']}")
    print(f"Effects open: {page['effects']['open']}")
    print(f"Sound: {page['sound']['title']}")
    print(f"Speed: {page['speed']['selected']}")
    print("Tools:")

    for tool in page["tools"]:
        print(
            f"  - {tool['label']} | "
            f"value={tool['value']} | "
            f"selected={tool['selected']}"
        )


async def render_shorts_camera_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    camera_state: str,
    camera_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE SHORTS CAMERA] "
                f"sample={sample_index} "
                f"state={camera_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"shorts_camera{camera_state}",
                template_name="pages/shorts_camera.html",
                context_key="page",
                page_data=camera_page,
                system=None,
                theme=theme,
                viewport=viewport,
                output_subdir="shorts_camera",
                # (
                #     f"shorts_camera/"
                #     f"{theme_mode}/"
                #     f"{camera_state}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": camera_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE SHORTS CAMERA FAILED] "
                f"sample={sample_index} "
                f"state={camera_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": camera_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_camera_states()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE SHORTS CAMERA")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Camera states: {CAMERA_STATES_TO_RENDER}")
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
        desc="YouTube Shorts Camera",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for camera_state in CAMERA_STATES_TO_RENDER:
            camera_page = generate_shorts_camera_page(
                state=camera_state,
            )

            print("\n======================================")
            print_page_debug(camera_page)

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_shorts_camera_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            camera_state=camera_state,
                            camera_page=camera_page,
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
        f"[YOUTUBE SHORTS CAMERA COMPLETE] "
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