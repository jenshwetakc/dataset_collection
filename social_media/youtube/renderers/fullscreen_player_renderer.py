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
from social_media.youtube.generators.fullscreen_player_generator import (
    PLAYER_STATES,
    generate_fullscreen_player_page,
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
# Player States
# ==========================================================

PLAYER_STATES_TO_RENDER = [
    "controls_visible",
    "controls_hidden",
    "paused",
    "seeking_backward",
    "seeking_forward",
]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
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


# ==========================================================
# Scroll and Capture Configuration
# ==========================================================

SCROLL_PERCENTAGES = [
    0,
]

SAVE_FULL_PAGE = False
SAVE_VIEWPORTS = True


# ==========================================================
# Validation
# ==========================================================

def validate_player_states() -> None:
    unknown_states = [
        state
        for state in PLAYER_STATES_TO_RENDER
        if state not in PLAYER_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown player states: "
            f"{unknown_states}. "
            f"Available states: {PLAYER_STATES}"
        )


async def render_fullscreen_player_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    player_state: str,
    player_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE FULLSCREEN PLAYER] "
                f"sample={sample_index} "
                f"state={player_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"fullscreen_{['player_state']}",
                template_name="pages/fullscreen_player.html",
                context_key="page",
                page_data=player_page,
                system=None,
                theme=theme,
                viewport=viewport,
                output_subdir="fullscreen_player",
                # (
                #     f"fullscreen_player/"
                #     f"{theme_mode}/"
                #     f"{player_state}"
                # ),
                annotation_profiles=ANNOTATION_PROFILES,
                scroll_percentages=SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": player_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE FULLSCREEN PLAYER FAILED] "
                f"sample={sample_index} "
                f"state={player_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": player_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_player_states()

    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE FULLSCREEN PLAYER")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Player states: {PLAYER_STATES_TO_RENDER}")
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
        desc="YouTube Fullscreen Player",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for player_state in PLAYER_STATES_TO_RENDER:
            player_page = generate_fullscreen_player_page(
                state=player_state,
            )
            video = player_page["video"]

            print("\n======================================")
            print(f"Player state: {player_state}")
            print(f"Video: {video['title']}")
            print(
                f"Playback: {video['current_time_text']} / "
                f"{video['duration_text']}"
            )
            print(f"Progress: {video['progress_percent']}%")
            print(f"Paused: {player_page['playback']['paused']}")
            print(
                "Controls visible: "
                f"{player_page['playback']['controls_visible']}"
            )

            if player_page["seek_feedback"]:
                print(
                    "Seek feedback: "
                    f"{player_page['seek_feedback']['direction']} "
                    f"{player_page['seek_feedback']['seconds']}s"
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
                        render_fullscreen_player_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            player_state=player_state,
                            player_page=player_page,
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
        f"[YOUTUBE FULLSCREEN PLAYER COMPLETE] "
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