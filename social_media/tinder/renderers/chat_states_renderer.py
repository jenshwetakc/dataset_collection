from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
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

from social_media.tinder.generators.chat_states_generator import (
    CHAT_STATES,
    generate_chat_states_data,
)

from social_media.tinder.renderers.common_renderer import (
    render_tinder_page,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 30

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

THEME_MODES = [
    "light",
    "dark",
]

CAPTURE_FULL_PAGE = False

CAPTURE_VIEWPORTS = True
DEFAULT_SAVE_VISUALIZATIONS = True
SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

TINDER_SEEDS = [
    "#FD5068",
    "#FF4458",
    "#FE3C72",
    "#E94057",
]

# Begin with 4 concurrent rendering jobs.
MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Render One Parallel Tinder State Job
# ==========================================================

async def render_one_tinder_state_job(
    browser,
    semaphore,
    state: str,
    state_sample_index: int,
    global_sample_index: int,
    chat_data: dict,
    system: dict,
    theme: dict,
    theme_mode: str,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                "\n"
                "===================================="
            )

            print("TINDER CHAT STATE")
            print("State:", state)
            print("State sample:", state_sample_index)
            print("Global sample:", global_sample_index)
            print("Theme:", theme_mode)
            print("Viewport:", viewport["name"])

            print(
                "===================================="
            )

            # Pass the shared Browser directly.
            # The common renderer creates one page per job
            # and closes it after that job finishes.
            await render_tinder_page(

                browser=browser,

                sample_index=global_sample_index,

                page_type=f"chat_{state}",

                template_name="chat_states.html",

                context_key="chat",

                page_data=chat_data,

                system=system,

                theme=theme,

                viewport=viewport,

                output_subdir="chat_states",

                annotation_profiles=ANNOTATION_PROFILES,

                capture_full_page=CAPTURE_FULL_PAGE,

                capture_viewports=CAPTURE_VIEWPORTS,

                scroll_percentages=SCROLL_PERCENTAGES,

            )

            return {

                "status": "success",

                "state": state,

                "state_sample_index": state_sample_index,

                "global_sample_index": global_sample_index,

                "theme": theme_mode,

                "viewport": viewport["name"],
            }

        except Exception as error:

            return {

                "status": "failed",

                "state": state,

                "state_sample_index": state_sample_index,

                "global_sample_index": global_sample_index,

                "theme": theme_mode,

                "viewport": viewport["name"],

                "error": str(error),
            }


# ==========================================================
# Main Generation
# ==========================================================

async def main(
    browser,
):

    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS
    )

    jobs = []

    total_jobs = (

        len(CHAT_STATES)

        * NUM_SAMPLES_PER_STATE

        * len(THEME_MODES)

        * len(viewports)
    )

    print(
        "\n"
        "===================================="
    )

    print("Tinder Chat States Dataset Generation")
    print("States:", len(CHAT_STATES))
    print(
        "Samples per state:",
        NUM_SAMPLES_PER_STATE,
    )
    print("Themes:", len(THEME_MODES))
    print("Viewports:", len(viewports))
    print("Total jobs:", total_jobs)

    print(
        "Parallel workers:",
        MAX_CONCURRENT_WORKERS,
    )

    print(
        "===================================="
    )


    # One state UI variation is generated per state/sample.
    # It is then captured in both themes and all viewports.
    global_sample_index = 0


    for state in CHAT_STATES:

        for state_sample_index in range(
            NUM_SAMPLES_PER_STATE,
        ):

            chat_data = generate_chat_states_data(
                state=state,
            )

            system = generate_system_data()

            for theme_mode in THEME_MODES:

                theme = generate_accessible_theme(

                    seed=random.choice(
                        TINDER_SEEDS
                    ),

                    mode=theme_mode,
                )

                for viewport in viewports:

                    jobs.append(

                        render_one_tinder_state_job(

                            browser=browser,

                            semaphore=semaphore,

                            state=state,

                            state_sample_index=state_sample_index,

                            global_sample_index=global_sample_index,

                            chat_data=chat_data,

                            system=system,

                            theme=theme,

                            theme_mode=theme_mode,

                            viewport=viewport,
                        )
                    )

            # Increment only after all themes and viewports
            # for this one state variation are scheduled.
            global_sample_index += 1


    results = await asyncio.gather(
        *jobs
    )


    successful_results = [

        result

        for result in results

        if result["status"] == "success"
    ]


    failed_results = [

        result

        for result in results

        if result["status"] == "failed"
    ]


    print(
        "\n"
        "===================================="
    )

    print("Generation complete")

    print(
        "Successful jobs:",
        len(successful_results),
    )

    print(
        "Failed jobs:",
        len(failed_results),
    )

    print(
        "===================================="
    )


    for result in failed_results:

        print(

            "[FAILED]",

            "State:",
            result["state"],

            "| Global sample:",
            result["global_sample_index"],

            "| Theme:",
            result["theme"],

            "| Viewport:",
            result["viewport"],

            "| Error:",
            result["error"],
        )


# ==========================================================
# Browser Lifecycle
# ==========================================================

async def run():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:

            await main(
                browser
            )

        finally:

            await browser.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )