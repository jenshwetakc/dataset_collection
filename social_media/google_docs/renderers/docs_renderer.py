from __future__ import annotations

import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.google_docs.generators.docs_generator import (
    generate_docs_page,
)

from social_media.google_docs.renderers.common_renderer import (
    render_google_docs_page,
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

SAVE_VISUALIZATIONS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Theme Generator
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
# Render One Docs Job
# ==========================================================

async def render_docs_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    docs: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:

    async with semaphore:

        try:

            print(
                f"[GOOGLE DOCS] "
                f"sample={sample_index} "
                f"state={docs['state']} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_google_docs_page(
                browser=browser,
                sample_index=sample_index,
                page_type="docs",
                template_name="docs.html",
                context_key="docs",
                page_data=docs,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="docs",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
                save_visualizations=SAVE_VISUALIZATIONS,
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "state": docs["state"],
                "viewport": viewport["name"],
            }

        except Exception as error:

            print(
                f"[GOOGLE DOCS FAILED] "
                f"sample={sample_index} "
                f"state={docs['state']} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {
                "status": "failed",
                "sample_index": sample_index,
                "state": docs["state"],
                "viewport": viewport["name"],
                "error": str(error),
            }


# ==========================================================
# Render Dataset
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

    for sample_index in range(NUM_SAMPLES):

        docs = generate_docs_page()

        system = generate_system_data()

        theme = generate_theme()

        print(
            "\n=========================================="
        )

        print(
            "GOOGLE DOCS SAMPLE",
            sample_index,
        )

        print(
            "State:",
            docs["state"],
        )

        print(
            "Document:",
            docs["document"]["title"],
        )

        print(
            "Sections:",
            len(
                docs["document"]["sections"]
            ),
        )

        print(
            "Collaborators:",
            len(
                docs["collaborators"]
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
                render_docs_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    docs=docs,
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

    failed = len(results) - successful

    print(
        f"[GOOGLE DOCS COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
    )


# ==========================================================
# Browser Entry Point
# ==========================================================

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