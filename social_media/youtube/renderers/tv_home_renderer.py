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
from social_media.youtube.generators.tv_home_generator import (
    TV_HOME_STATES,
    generate_tv_home_page,
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
# TV States
# ==========================================================

TV_STATES_TO_RENDER = [
    "home",
    "navigation_focused",
    "video_focused",
    "profile_menu",
    "search_focused",
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


def validate_tv_states() -> None:
    unknown_states = [
        state
        for state in TV_STATES_TO_RENDER
        if state not in TV_HOME_STATES
    ]

    if unknown_states:
        raise ValueError(
            "Unknown TV home states: "
            f"{unknown_states}. "
            f"Available states: {TV_HOME_STATES}"
        )


def print_page_debug(page: dict) -> None:
    print(f"State: {page['state']}")
    print(f"Hero visible: {page['layout']['show_hero']}")
    print(f"Rows visible: {page['layout']['show_rows']}")
    print(f"Profile menu: {page['profile_menu']['open']}")
    print(
        "Search overlay: "
        f"{page['layout']['show_search_overlay']}"
    )
    print(f"Rows: {len(page['rows'])}")
    print("Navigation:")

    for item in page["navigation"]:
        print(
            f"  - {item['label']} | "
            f"selected={item['selected']} | "
            f"focused={item['focused']}"
        )

    print("Content rows:")

    for row in page["rows"]:
        focused_items = [
            video["title"]
            for video in row["items"]
            if video["focused"]
        ]

        print(
            f"  - {row['title']} | "
            f"items={len(row['items'])} | "
            f"focused={focused_items}"
        )

    print(f"Profiles: {len(page['profiles'])}")
    print(f"Search query: {page['search']['query']!r}")
    print(
        "Search suggestions: "
        f"{len(page['search']['suggestions'])}"
    )


async def render_tv_home_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    tv_state: str,
    tv_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE TV HOME] "
                f"sample={sample_index} "
                f"state={tv_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"tv_home{tv_state}",
                template_name="pages/tv_home.html",
                context_key="page",
                page_data=tv_page,
                system=None,
                theme=theme,
                viewport=viewport,

                output_subdir="tv_home",
                # (
                #     f"tv_home/"
                #     f"{theme_mode}/"
                #     f"{tv_state}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,

            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": tv_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE TV HOME FAILED] "
                f"sample={sample_index} "
                f"state={tv_state} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": tv_state,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_tv_states()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE TV HOME")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"TV states: {TV_STATES_TO_RENDER}")
    print(f"Themes: {THEME_MODES}")
    print(f"Save full page: {SAVE_FULL_PAGE}")
    print(f"Save viewport: {SAVE_VIEWPORTS}")
    print(f"Scroll positions: {SCROLL_PERCENTAGES}")
    print("\nTesting TV viewports:")

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
        desc="YouTube TV Home",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for tv_state in TV_STATES_TO_RENDER:
            tv_page = generate_tv_home_page(
                state=tv_state,
            )

            print("\n======================================")
            print_page_debug(tv_page)

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_tv_home_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            tv_state=tv_state,
                            tv_page=tv_page,
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
        f"[YOUTUBE TV HOME COMPLETE] "
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