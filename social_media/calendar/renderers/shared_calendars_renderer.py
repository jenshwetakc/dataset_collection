from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.calendar.generators.shared_calendars_generator import (
    SHARED_CALENDAR_STATES,
    generate_shared_calendars_data,
)

from social_media.calendar.renderers.common_renderer import (
    render_calendar_page,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.system_generator import (
    generate_system_data,
)

from social_media.common.viewport import (
    get_viewports_by_names,
)


# ==========================================================
# Dataset Configuration
# ==========================================================

NUM_SAMPLES = 25

SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_android",
    "standard_iphone",
    "large_mobile",
    "mobile_landscape",
    "tablet_portrait",
    "large_tablet_portrait",
    "tablet_landscape",
    "foldable",
    "small_laptop",
    "laptop",
    "large_laptop",
    "desktop_fhd",
    "desktop_qhd",
    "desktop_4k",
    "ultrawide",
]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

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


# ==========================================================
# Theme
# ==========================================================

def generate_theme() -> dict:
    mode = (
        random.choice([
            "light",
            "dark",
        ])
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render Job
# ==========================================================

async def render_shared_calendars_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    calendar: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[SHARED CALENDARS] "
                f"sample={sample_index} "
                f"state={calendar['state']} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_calendar_page(
                browser=browser,

                sample_index=
                    sample_index,

                page_type=(
                    "shared_calendars_"
                    f"{calendar['state']}"
                ),

                template_name=
                    "shared_calendars.html",

                context_key=
                    "calendar",

                page_data=
                    calendar,

                system=
                    system,

                theme=
                    theme,

                viewport=
                    viewport,

                output_subdir=
                    "shared_calendars",

                annotation_profiles=
                    ANNOTATION_PROFILES,

                capture_full_page=
                    CAPTURE_FULL_PAGE,

                capture_viewports=
                    CAPTURE_VIEWPORTS,

                scroll_percentages=
                    SCROLL_PERCENTAGES,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": calendar["state"],
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[SHARED CALENDARS FAILED] "
                f"sample={sample_index} "
                f"state={calendar['state']} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": calendar["state"],
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Main
# ==========================================================

async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    for sample_index in range(NUM_SAMPLES):
        state = SHARED_CALENDAR_STATES[
            sample_index
            % len(SHARED_CALENDAR_STATES)
        ]

        calendar = (
            generate_shared_calendars_data(
                state=state
            )
        )

        system = generate_system_data()
        theme = generate_theme()

        print(
            "\n======================================"
        )
        print(
            "SHARED CALENDAR SAMPLE",
            sample_index,
        )
        print(
            "State:",
            calendar["state"],
        )
        print(
            "Members:",
            calendar["all_members_count"],
        )
        print(
            "Popup:",
            calendar["popup_open"],
        )
        print(
            "Theme:",
            theme["mode"],
        )
        print(
            "======================================"
        )

        for viewport in viewports:
            jobs.append(
                render_shared_calendars_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    calendar=calendar,
                    system=system,
                    theme=theme,
                    viewport=viewport,
                )
            )

    results = await asyncio.gather(
        *jobs
    )

    successful = sum(
        result["status"] == "success"
        for result in results
    )

    failed = (
        len(results)
        - successful
    )

    print(
        f"[SHARED CALENDARS COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
    )


# ==========================================================
# Runner
# ==========================================================

async def run() -> None:
    async with async_playwright() as playwright:
        browser = (
            await playwright.chromium.launch(
                headless=True,
            )
        )

        try:
            await main(browser)

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())