from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.google_sheets.generators.spreadsheet_generator import (
    SPREADSHEET_STATES,
    generate_spreadsheet_data,
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
    # "desktop_4k",
]


ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]


# Supported:
#     "light"
#     "dark"
#     "random"

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


# Maximum number of simultaneous Playwright pages.
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
            "'light', 'dark', or 'random'. "
            f"Received: {THEME_MODE}"
        )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render One Spreadsheet Job
# ==========================================================

async def render_spreadsheet_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    spreadsheet: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        state = spreadsheet[
            "state"
        ]

        viewport_name = viewport[
            "name"
        ]

        theme_mode = theme[
            "mode"
        ]

        try:

            print(
                f"[GOOGLE SHEETS] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport_name} "
                f"theme={theme_mode}"
            )

            result = await render_google_sheets_page(

                browser=
                    browser,

                sample_index=
                    sample_index,

                # Including the state in page_type makes
                # every state identifiable in its filename.
                page_type=
                    f"spreadsheet_{state}",

                template_name=
                    "spreadsheet.html",

                context_key=
                    "spreadsheet",

                page_data=
                    spreadsheet,

                system=
                    system,

                theme=
                    theme,

                viewport=
                    viewport,

                # All spreadsheet states are stored under
                # the same output directory.
                output_subdir=
                    "spreadsheet",

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

                "theme":
                    theme_mode,

                "result":
                    result,
            }

        except Exception as error:

            print(
                f"[GOOGLE SHEETS FAILED] "
                f"sample={sample_index} "
                f"state={state} "
                f"viewport={viewport_name} "
                f"theme={theme_mode} "
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

                "theme":
                    theme_mode,

                "error":
                    str(error),
            }


# ==========================================================
# Main Rendering Logic
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


    # ======================================================
    # Generate Samples
    # ======================================================

    for sample_index in range(
        NUM_SAMPLES
    ):

        # Cycle through the state list so all states are
        # generated before any state repeats.
        state = SPREADSHEET_STATES[
            sample_index
            % len(
                SPREADSHEET_STATES
            )
        ]

        # Generate one spreadsheet sample.
        #
        # Do not pass a viewport here. This ensures the same
        # spreadsheet data is rendered on every viewport.
        # Responsive behavior is handled by the HTML/CSS.
        spreadsheet = generate_spreadsheet_data(

            state=
                state,

            seed=
                sample_index,
        )

        # Generate one system state and one theme per sample.
        # These are reused for every viewport.
        system = generate_system_data()

        theme = generate_theme()


        print(
            "\n"
            "=========================================="
        )

        print(
            "GOOGLE SHEETS SAMPLE",
            sample_index,
        )

        print(
            "State:",
            spreadsheet[
                "state"
            ],
        )

        print(
            "Title:",
            spreadsheet[
                "title"
            ],
        )

        print(
            "Rows:",
            len(
                spreadsheet[
                    "rows"
                ]
            ),
        )

        print(
            "Columns:",
            len(
                spreadsheet[
                    "column_letters"
                ]
            ),
        )

        print(
            "Selected cell:",
            spreadsheet[
                "selected_cell"
            ],
        )

        print(
            "Sheets:",
            len(
                spreadsheet[
                    "sheet_tabs"
                ]
            ),
        )

        print(
            "Popup state:",
            spreadsheet[
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


        # ==================================================
        # Add One Job Per Viewport
        # ==================================================

        for viewport in viewports:

            jobs.append(

                render_spreadsheet_job(

                    browser=
                        browser,

                    semaphore=
                        semaphore,

                    sample_index=
                        sample_index,

                    spreadsheet=
                        spreadsheet,

                    system=
                        system,

                    theme=
                        theme,

                    viewport=
                        viewport,
                )
            )


    # ======================================================
    # Execute Jobs
    # ======================================================

    results = await asyncio.gather(
        *jobs
    )


    # ======================================================
    # Summary
    # ======================================================

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
        "\n"
        "=========================================="
    )

    print(
        "GOOGLE SHEETS RENDERING COMPLETE"
    )

    print(
        "=========================================="
    )

    print(
        "Samples:",
        NUM_SAMPLES,
    )

    print(
        "Viewports per sample:",
        len(
            viewports
        ),
    )

    print(
        "Total jobs:",
        len(
            results
        ),
    )

    print(
        "Successful:",
        successful,
    )

    print(
        "Failed:",
        failed,
    )


    # ======================================================
    # Failed Job Details
    # ======================================================

    if failed > 0:

        print(
            "\n"
            "FAILED JOBS"
        )

        for result in results:

            if result[
                "status"
            ] != "failed":

                continue

            print(
                f"- sample="
                f"{result['sample_index']} "
                f"state="
                f"{result['state']} "
                f"viewport="
                f"{result['viewport']} "
                f"error="
                f"{result['error']}"
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


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    asyncio.run(
        run()
    )