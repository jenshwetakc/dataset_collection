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
from social_media.youtube.generators.upload_generator import (
    UPLOAD_STATES,
    generate_upload_video_page,
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
# Upload States
# ==========================================================

UPLOAD_STATES_TO_RENDER = [
    "select_file",
    "uploading",
    "details",
    "processing",
    "ready_to_publish",
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
    25,
    50,
    75,
    100,
]

SAVE_FULL_PAGE = True
SAVE_VIEWPORTS = True


def validate_upload_states() -> None:
    unknown_states = [
        state
        for state in UPLOAD_STATES_TO_RENDER
        if state not in UPLOAD_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown upload states: "
            f"{unknown_states}. "
            f"Available states: {UPLOAD_STATES}"
        )


def print_page_debug(page: dict) -> None:
    print(f"File: {page['file']['filename']}")
    print(f"Size: {page['file']['size_text']}")
    print(f"Duration: {page['file']['duration_text']}")
    print(f"Resolution: {page['file']['resolution']}")
    print(f"Upload status: {page['progress']['status']}")
    print(f"Upload percent: {page['progress']['percent']}%")
    print(f"Visibility: {page['visibility']['selected']}")
    print(f"Made for kids: {page['audience']['made_for_kids']}")
    print("Layout:")

    for key, value in page["layout"].items():
        print(f"  {key}: {value}")


async def render_upload_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    upload_state: str,
    upload_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE UPLOAD] "
                f"sample={sample_index} "
                f"state={upload_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"upload{upload_state}",
                template_name="pages/upload.html",
                context_key="page",
                page_data=upload_page,
                system=None,
                theme=theme,
                viewport=viewport,

                output_subdir="upload",
                # (
                #     f"upload/"
                #     f"{theme_mode}/"
                #     f"{upload_state}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": upload_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE UPLOAD FAILED] "
                f"sample={sample_index} "
                f"state={upload_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": upload_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_upload_states()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE UPLOAD VIDEO")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Upload states: {UPLOAD_STATES_TO_RENDER}")
    print(f"Themes: {THEME_MODES}")
    print(f"Full-page capture: {SAVE_FULL_PAGE}")
    print(f"Viewport capture: {SAVE_VIEWPORTS}")
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
        desc="YouTube Upload",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for upload_state in UPLOAD_STATES_TO_RENDER:
            upload_page = generate_upload_video_page(
                state=upload_state,
            )

            print("\n======================================")
            print(f"Upload state: {upload_state}")
            print_page_debug(upload_page)

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_upload_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            upload_state=upload_state,
                            upload_page=upload_page,
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
        f"[YOUTUBE UPLOAD COMPLETE] "
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