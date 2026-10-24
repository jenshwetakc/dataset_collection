from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.google_sheets.generators.template_gallery_generator import (
    TEMPLATE_GALLERY_STATES,
    generate_template_gallery_data,
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
# Configuration
# ==========================================================

NUM_SAMPLES_PER_STATE = 25


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
# Theme
# ==========================================================

def generate_theme() -> dict:

    mode = (
        random.choice(
            [
                "light",
                "dark",
            ]
        )
        if THEME_MODE == "random"
        else THEME_MODE
    )

    return generate_accessible_theme(
        mode=mode
    )


# ==========================================================
# Render One Job
# ==========================================================

async def render_template_gallery_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    template_gallery: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                f"[SHEETS TEMPLATE GALLERY] "
                f"sample={sample_index} "
                f"state={template_gallery['state']} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            result = await render_google_sheets_page(

                browser=
                    browser,

                sample_index=
                    sample_index,

                page_type=
                    "template_gallery",

                template_name=
                    "template_gallery.html",

                context_key=
                    "template_gallery",

                page_data=
                    template_gallery,

                system=
                    system,

                theme=
                    theme,

                viewport=
                    viewport,

                output_subdir=
                    "template_gallery",

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
                    template_gallery["state"],
                "viewport":
                    viewport["name"],
                "result":
                    result,
            }

        except Exception as error:

            print(
                f"[SHEETS TEMPLATE GALLERY FAILED] "
                f"sample={sample_index} "
                f"state={template_gallery['state']} "
                f"viewport={viewport['name']} "
                f"error={error!r}"
            )

            return {
                "status":
                    "failed",
                "sample_index":
                    sample_index,
                "state":
                    template_gallery["state"],
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

    sample_index = 0

    for state in TEMPLATE_GALLERY_STATES:

        for state_sample_index in range(
            NUM_SAMPLES_PER_STATE
        ):

            template_gallery = (
                generate_template_gallery_data(
                    state=state
                )
            )

            system = (
                generate_system_data()
            )

            theme = (
                generate_theme()
            )

            print(
                "\n=========================================="
            )

            print(
                "GOOGLE SHEETS TEMPLATE GALLERY"
            )

            print(
                "Sample:",
                sample_index,
            )

            print(
                "State:",
                state,
            )

            print(
                "State sample:",
                state_sample_index,
            )

            print(
                "Visible templates:",
                len(
                    template_gallery["templates"]
                ),
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

                    render_template_gallery_job(

                        browser=
                            browser,

                        semaphore=
                            semaphore,

                        sample_index=
                            sample_index,

                        template_gallery=
                            template_gallery,

                        system=
                            system,

                        theme=
                            theme,

                        viewport=
                            viewport,
                    )
                )

            sample_index += 1

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
        "\n=========================================="
    )

    print(
        "TEMPLATE GALLERY COMPLETE"
    )

    print(
        "Successful:",
        successful,
    )

    print(
        "Failed:",
        failed,
    )

    print(
        "Total:",
        len(results),
    )

    print(
        "=========================================="
    )


# ==========================================================
# Run
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