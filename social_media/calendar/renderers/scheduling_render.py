from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.calendar.generators.scheduling_generator import (
    SCHEDULING_STATES,
    generate_scheduling_data,
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
# Configuration
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


SELECTED_STATES: list[str] | None = None


# ==========================================================
# Theme
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
            f"Invalid THEME_MODE: {THEME_MODE}"
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

    states = (
        SELECTED_STATES
        if SELECTED_STATES is not None
        else SCHEDULING_STATES
    )

    if not states:

        raise ValueError(
            "No scheduling states selected."
        )

    invalid_states = [
        state
        for state in states
        if state not in SCHEDULING_STATES
    ]

    if invalid_states:

        raise ValueError(
            f"Unknown scheduling states: "
            f"{invalid_states}"
        )

    # Cycle through states so every state is generated.
    return states[
        sample_index
        % len(states)
    ]


# ==========================================================
# Render Job
# ==========================================================

async def render_scheduling_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    scheduling_data: dict,
    system_data: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        state = scheduling_data[
            "state"
        ]

        try:

            print(
                f"[SCHEDULING] "
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

                page_type=
                    f"scheduling_{state}",

                template_name=
                    "scheduling.html",

                context_key=
                    "scheduling",

                page_data=
                    scheduling_data,

                system=
                    system_data,

                theme=
                    theme,

                viewport=
                    viewport,

                output_subdir=
                    "scheduling",

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
            }

        except Exception as error:

            print(
                f"[SCHEDULING FAILED] "
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
# Main
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

        scheduling_data = (
            generate_scheduling_data(
                state=state,
                seed=sample_index,
            )
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
            "SCHEDULING SAMPLE:",
            sample_index,
        )

        print(
            "State:",
            scheduling_data["state"],
        )

        print(
            "Participants:",
            scheduling_data[
                "participant_count"
            ],
        )

        print(
            "Time slots:",
            len(
                scheduling_data[
                    "time_slots"
                ]
            ),
        )

        print(
            "Popup:",
            scheduling_data[
                "popup_open"
            ],
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
                render_scheduling_job(

                    browser=
                        browser,

                    semaphore=
                        semaphore,

                    sample_index=
                        sample_index,

                    scheduling_data=
                        scheduling_data,

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
        "[SCHEDULING COMPLETE]"
    )

    print(
        f"Successful: {successful}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        "=========================================="
    )


# ==========================================================
# Entry Point
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