from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.google_sheets.generators.home_generator import (
    HOME_STATES,
    generate_home_data,
)

from social_media.google_sheets.renderers.common_renderer import (
    render_google_sheets_page,
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

    else:

        mode = THEME_MODE

    if mode not in {
        "light",
        "dark",
    }:

        raise ValueError(
            "THEME_MODE must be "
            "'light', 'dark', or 'random'."
        )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render Job
# ==========================================================

async def render_home_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    sheets_home: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        state = sheets_home[
            "state"
        ]

        viewport_name = viewport[
            "name"
        ]

        try:

            print(
                f"[GOOGLE SHEETS HOME] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport_name} "
                f"theme={theme['mode']}"
            )

            result = await render_google_sheets_page(

                browser=
                    browser,

                sample_index=
                    sample_index,

                page_type=
                    f"home_{state}",

                template_name=
                    "home.html",

                context_key=
                    "sheets_home",

                page_data=
                    sheets_home,

                system=
                    system,

                theme=
                    theme,

                viewport=
                    viewport,

                output_subdir=
                    "home",

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
                    viewport_name,

                "result":
                    result,
            }

        except Exception as error:

            print(
                f"[GOOGLE SHEETS HOME FAILED] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport_name} "
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
                    viewport_name,

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

        state = HOME_STATES[
            sample_index
            % len(
                HOME_STATES
            )
        ]

        sheets_home = generate_home_data(
            state=state,
            seed=sample_index,
        )

        system = generate_system_data()

        theme = generate_theme()

        print(
            "\n"
            "=========================================="
        )

        print(
            "GOOGLE SHEETS HOME SAMPLE",
            sample_index,
        )

        print(
            "State:",
            sheets_home[
                "state"
            ],
        )

        print(
            "Files:",
            len(
                sheets_home[
                    "files"
                ]
            ),
        )

        print(
            "View mode:",
            sheets_home[
                "view_mode"
            ],
        )

        print(
            "Popup:",
            sheets_home[
                "is_popup"
            ],
        )

        print(
            "Theme:",
            theme[
                "mode"
            ],
        )

        print(
            "=========================================="
        )

        for viewport in viewports:

            jobs.append(

                render_home_job(

                    browser=
                        browser,

                    semaphore=
                        semaphore,

                    sample_index=
                        sample_index,

                    sheets_home=
                        sheets_home,

                    system=
                        system,

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

        result[
            "status"
        ]
        == "success"

        for result in results
    )

    failed = (
        len(
            results
        )
        - successful
    )

    print(
        f"[GOOGLE SHEETS HOME COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
    )


# ==========================================================
# Browser Runner
# ==========================================================

async def run() -> None:

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


if __name__ == "__main__":

    asyncio.run(
        run()
    )