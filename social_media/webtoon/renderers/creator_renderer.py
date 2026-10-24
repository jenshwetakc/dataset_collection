from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.dynamic_system_generator import (
    generate_system_data,
)
from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.viewport import get_viewports_by_names
from social_media.webtoon.generators.creator_generator import (
    CREATOR_STATES,
    apply_creator_state,
    generate_creator_data,
)
from social_media.webtoon.renderers.common_renderer import (
    render_webtoon_page,
)


NUM_SAMPLES = 5

VIEWPORTS = [
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

PAGE_STATES = CREATOR_STATES.copy()

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]

MAX_CONCURRENT_WORKERS = 4


def generate_theme() -> dict:
    if THEME_MODE not in {"random", "light", "dark"}:
        raise ValueError(f"Invalid THEME_MODE: {THEME_MODE}")

    mode = (
        random.choice(["light", "dark"])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(mode=mode)


async def render_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    creator: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = creator["state"]

        try:
            print(
                "[WEBTOON CREATOR]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"theme={theme['mode']}",
            )

            await render_webtoon_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f"creator_{state}",
                template_name="creator.html",
                context_key="webtoon",
                page_data=creator,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="creator",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=(
                    [0]
                    if creator["popup"] or creator["menu_open"]
                    else SCROLL_PERCENTAGES
                ),
            )

            return {
                "status": "success",
                "state": state,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                "[WEBTOON CREATOR FAILED]",
                f"sample={sample_index}",
                f"state={state}",
                f"viewport={viewport['name']}",
                f"error={error!r}",
            )

            return {
                "status": "failed",
                "state": state,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError("MAX_CONCURRENT_WORKERS must be positive.")

    if not CAPTURE_FULL_PAGE and not CAPTURE_VIEWPORTS:
        raise ValueError("Enable at least one capture mode.")

    unknown_states = set(PAGE_STATES) - set(CREATOR_STATES)

    if unknown_states:
        raise ValueError(f"Unknown creator states: {unknown_states}")

    viewports = get_viewports_by_names(VIEWPORTS)

    if not viewports or not PAGE_STATES:
        raise ValueError("Select at least one viewport and state.")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)

    total_successful = 0
    total_failed = 0

    for sample_index in range(NUM_SAMPLES):
        content = generate_creator_data()
        theme = generate_theme()

        states = [
            apply_creator_state(content, state)
            for state in PAGE_STATES
        ]

        jobs = []

        for viewport in viewports:
            system = generate_system_data(viewport=viewport)

            for creator in states:
                jobs.append(
                    render_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        creator=creator,
                        system=system,
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

        total_successful += successful
        total_failed += failed

        print(
            "[WEBTOON CREATOR SAMPLE COMPLETE]",
            f"sample={sample_index}",
            f"successful={successful}",
            f"failed={failed}",
        )

    print(
        "\n[WEBTOON CREATOR COMPLETE]",
        f"successful={total_successful}",
        f"failed={total_failed}",
    )

    if total_failed:
        raise RuntimeError(
            f"{total_failed} creator jobs failed."
        )


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())