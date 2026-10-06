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
from social_media.youtube.generators.settings_generator import (
    SETTINGS_SECTIONS,
    generate_settings_page,
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
# Settings Sections
# ==========================================================

SETTINGS_SECTIONS_TO_RENDER = [
    "account",
    "notifications",
    "playback",
    "downloads",
    "privacy",
    "connected_apps",
    "billing",
    "advanced",
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


def validate_settings_sections() -> None:
    available_sections = {
        section["id"]
        for section in SETTINGS_SECTIONS
    }

    unknown_sections = [
        section
        for section in SETTINGS_SECTIONS_TO_RENDER
        if section not in available_sections
    ]

    if unknown_sections:
        raise ValueError(
            "Unknown settings sections: "
            f"{unknown_sections}. "
            f"Available sections: {sorted(available_sections)}"
        )


def print_page_debug(page: dict) -> None:
    print(f"Selected section: {page['selected_section']}")
    print(f"Title: {page['content']['title']}")
    print(f"Groups: {len(page['content']['groups'])}")
    print(f"User: {page['user']['name']}")
    print("Groups:")

    for group in page["content"]["groups"]:
        print(
            f"  - {group['title']} | "
            f"type={group['type']}"
        )

        if group["type"] in {"settings", "apps"}:
            print(f"    items: {len(group.get('items', []))}")


async def render_settings_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    selected_section: str,
    settings_page: dict,
    theme_mode: str,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[YOUTUBE SETTINGS] "
                f"sample={sample_index} "
                f"section={selected_section} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']}"
            )

            await render_youtube_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"settings{selected_section}",
                template_name="pages/settings.html",
                context_key="page",
                page_data=settings_page,
                system=None,
                theme=theme,
                viewport=viewport,

                output_subdir="settings",
                # (
                #     f"settings/"
                #     f"{theme_mode}/"
                #     f"{selected_section}"
                # ),
                scroll_percentages=SCROLL_PERCENTAGES,
                annotation_profiles=ANNOTATION_PROFILES,

            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "section": selected_section,
                "theme": theme_mode,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[YOUTUBE SETTINGS FAILED] "
                f"sample={sample_index} "
                f"section={selected_section} "
                f"theme={theme_mode} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "section": selected_section,
                "theme": theme_mode,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    validate_settings_sections()

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\n==========================================")
    print("YOUTUBE SETTINGS")
    print("==========================================")
    print(f"Samples: {NUM_SAMPLES}")
    print(f"Settings sections: {SETTINGS_SECTIONS_TO_RENDER}")
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
        desc="YouTube Settings",
    ):
        print("\n------------------------------------------")
        print(f"Sample: {sample_index}")

        for selected_section in SETTINGS_SECTIONS_TO_RENDER:
            settings_page = generate_settings_page(
                selected_section=selected_section,
            )

            print("\n======================================")
            print(f"Settings section: {selected_section}")
            print_page_debug(settings_page)

            for theme_mode in THEME_MODES:
                theme = generate_accessible_theme(
                    mode=theme_mode,
                )

                print(f"\nTheme: {theme_mode}")
                print(f"Seed: {theme.get('seed')}")
                print(f"WCAG pass: {theme.get('wcag_pass')}")

                for viewport in viewports:
                    jobs.append(
                        render_settings_job(
                            browser=browser,
                            semaphore=semaphore,
                            sample_index=sample_index,
                            selected_section=selected_section,
                            settings_page=settings_page,
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
        f"[YOUTUBE SETTINGS COMPLETE] "
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