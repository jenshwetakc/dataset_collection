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
from social_media.youtube.generators.live_chat_generator import (
    LIVE_CHAT_STATES,
    generate_live_chat_page,
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
# Live Chat States
# ==========================================================

LIVE_CHAT_STATES_TO_RENDER = [
    "normal",
    "pinned_message",
    "super_chat",
    "members_only",
    "chat_paused",
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

SAVE_FULL_PAGE = True
SAVE_VIEWPORTS = True


def validate_live_chat_states() -> None:
    unknown_states = [
        state
        for state in LIVE_CHAT_STATES_TO_RENDER
        if state not in LIVE_CHAT_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown live chat states: "
            f"{unknown_states}. "
            f"Available states: {LIVE_CHAT_STATES}"
        )


def print_page_debug(page: dict) -> None:
    print(f"State: {page['state']}")
    print(f"Title: {page['livestream']['title']}")
    print(f"Channel: {page['livestream']['channel']['name']}")
    print(f"Viewers: {page['livestream']['viewer_count_text']}")
    print(f"Messages: {len(page['chat_messages'])}")
    print(
        "Pinned message: "
        f"{page['pinned_message'].get('enabled', False)}"
    )
    print(f"Chat paused: {page['chat_header']['paused']}")
    print(f"Members only: {page['chat_input']['members_only']}")
    print(f"Chat input enabled: {page['chat_input']['enabled']}")

    super_chat_count = sum(
        message["type"] == "super_chat"
        for message in page["chat_messages"]
    )
    print(f"Super chats: {super_chat_count}")


async def render_live_chat_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    live_chat_state: str,
    live_chat_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE LIVE CHAT] "
                f"sample={sample_index} "
                f"state={live_chat_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"live_chat{live_chat_state}",
                template_name="pages/live_chat.html",
                context_key="page",
                page_data=live_chat_page,
                system=None,
                theme=theme,
                viewport=viewport,
                output_subdir="live_chat",
                # (
                #     f"live_chat/"
                #     f"{theme_mode}/"
                #     f"{live_chat_state}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,

            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": live_chat_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE LIVE CHAT FAILED] "
                f"sample={sample_index} "
                f"state={live_chat_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": live_chat_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_live_chat_states()

    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE LIVE CHAT")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"States: {LIVE_CHAT_STATES_TO_RENDER}")
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
        desc="YouTube Live Chat",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for live_chat_state in LIVE_CHAT_STATES_TO_RENDER:
            live_chat_page = generate_live_chat_page(
                state=live_chat_state,
            )

            print("\n======================================")
            print_page_debug(live_chat_page)

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_live_chat_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            live_chat_state=live_chat_state,
                            live_chat_page=live_chat_page,
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
        f"[YOUTUBE LIVE CHAT COMPLETE] "
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