from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.calendar.generators.calendar_generator import (
    CALENDAR_STATES,
    generate_calendar_data,
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
    # "ultrawide",
]


ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# Supported:
#
# "light"
# "dark"
# "random"

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


SAVE_VISUALIZATIONS = True


MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Optional State Selection
# ==========================================================

# Use None to randomly choose from every state.
#
# Example:
#
# SELECTED_STATES = [
#     "month_view",
#     "week_view",
# ]

SELECTED_STATES: list[str] | None = None


# ==========================================================
# Theme Generator
# ==========================================================

def generate_theme() -> dict:

    if THEME_MODE == "random":

        mode = random.choice(
            [
                "light",
                "dark",
            ]
        )

    elif THEME_MODE in {
        "light",
        "dark",
    }:

        mode = THEME_MODE

    else:

        raise ValueError(
            f"Invalid THEME_MODE: {THEME_MODE}. "
            f"Expected 'light', 'dark', or 'random'."
        )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# State Resolver
# ==========================================================

def resolve_state(
    sample_index: int,
) -> str:

    if SELECTED_STATES is None:

        return random.choice(
            CALENDAR_STATES
        )

    if not SELECTED_STATES:

        raise ValueError(
            "SELECTED_STATES cannot be empty. "
            "Use None to enable all Calendar states."
        )

    invalid_states = [
        state
        for state in SELECTED_STATES
        if state not in CALENDAR_STATES
    ]

    if invalid_states:

        raise ValueError(
            f"Unknown Calendar states: "
            f"{invalid_states}. "
            f"Available states: "
            f"{CALENDAR_STATES}"
        )

    return SELECTED_STATES[
        sample_index
        % len(SELECTED_STATES)
    ]


# ==========================================================
# Render One Viewport
# ==========================================================

async def render_calendar_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    calendar_data: dict,
    system_data: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        state = calendar_data[
            "state"
        ]

        try:

            print(
                f"[CALENDAR] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_calendar_page(

                browser=
                    browser,

                sample_index=
                    sample_index,

                # Including the state in page_type gives
                # every state a distinct output filename.
                page_type=
                    f"calendar_{state}",

                template_name=
                    "calendar.html",

                context_key=
                    "calendar",

                page_data=
                    calendar_data,

                system=
                    system_data,

                theme=
                    theme,

                viewport=
                    viewport,

                # All Calendar states are saved under the
                # same output directory.
                output_subdir=
                    "calendar",

                annotation_profiles=
                    ANNOTATION_PROFILES,

                capture_full_page=
                    CAPTURE_FULL_PAGE,

                capture_viewports=
                    CAPTURE_VIEWPORTS,

                scroll_percentages=
                    SCROLL_PERCENTAGES,

                save_visualizations=
                    SAVE_VISUALIZATIONS,
            )

            return {
                "status":
                    "success",

                "sample_index":
                    sample_index,

                "state":
                    state,

                "viewport":
                    viewport["name"],

                "theme":
                    theme["mode"],
            }

        except Exception as error:

            print(
                f"[CALENDAR FAILED] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status":
                    "failed",

                "sample_index":
                    sample_index,

                "state":
                    state,

                "viewport":
                    viewport["name"],

                "error":
                    str(error),
            }


# ==========================================================
# Main Dataset Loop
# ==========================================================

async def main(
    browser,
) -> None:

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []


    for sample_index in range(
        NUM_SAMPLES
    ):

        state = resolve_state(
            sample_index
        )

        # Generate the Calendar page only once for a sample.
        # The same page data is rendered at every viewport,
        # which makes responsive comparison possible.
        calendar_data = generate_calendar_data(
            state=state,
            seed=sample_index,
        )

        system_data = (
            generate_system_data()
        )

        theme = generate_theme()


        print(
            "\n"
            "=========================================="
        )

        print(
            "CALENDAR SAMPLE",
            sample_index,
        )

        print(
            "State:",
            calendar_data["state"],
        )

        print(
            "View:",
            calendar_data["current_view"],
        )

        print(
            "Events:",
            len(
                calendar_data["events"]
            ),
        )

        print(
            "Popup:",
            calendar_data["popup_open"],
        )

        print(
            "Theme:",
            theme["mode"],
        )

        print(
            "=========================================="
        )


        for viewport in viewports:

            jobs.append(
                render_calendar_job(

                    browser=
                        browser,

                    semaphore=
                        semaphore,

                    sample_index=
                        sample_index,

                    calendar_data=
                        calendar_data,

                    system_data=
                        system_data,

                    theme=
                        theme,

                    viewport=
                        viewport,
                )
            )


    results = await asyncio.gather(
        *jobs
    )


    successful = sum(
        result["status"]
        == "success"
        for result in results
    )

    failed = (
        len(results)
        - successful
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "[CALENDAR COMPLETE]"
    )

    print(
        f"Samples: {NUM_SAMPLES}"
    )

    print(
        f"Viewports per sample: "
        f"{len(viewports)}"
    )

    print(
        f"Total jobs: "
        f"{len(results)}"
    )

    print(
        f"Successful: "
        f"{successful}"
    )

    print(
        f"Failed: "
        f"{failed}"
    )

    print(
        "=========================================="
    )


# ==========================================================
# Playwright Entry Point
# ==========================================================

async def run() -> None:

    async with async_playwright() as playwright:

        browser = (
            await playwright.chromium.launch(
                headless=True,
            )
        )

        try:

            await main(
                browser
            )

        finally:

            await browser.close()


if __name__ == "__main__":

    asyncio.run(
        run()
    )