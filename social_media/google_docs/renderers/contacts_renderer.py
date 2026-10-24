from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.common.system_generator import (
    generate_system_data,
)
from social_media.common.viewport import (
    get_viewports_by_names,
)
from social_media.google_docs.generators.contacts_generator import (
    CONTACT_STATES,
    generate_contacts_data,
)
from social_media.google_docs.renderers.common_renderer import (
    render_google_docs_page,
)


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
    "ultrawide",
]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

MAX_CONCURRENT_WORKERS = 4


def generate_theme() -> dict:
    return generate_accessible_theme(
        mode=random.choice(["light", "dark"]),
    )


async def render_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    contacts: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            await render_google_docs_page(
                browser=browser,
                sample_index=sample_index,
                page_type=(
                    f"contacts_{contacts['state']}"
                ),
                template_name="contacts.html",
                context_key="contacts",
                page_data=contacts,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="contacts",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=False,
                capture_viewports=True,
                scroll_percentages=[0],
                save_visualizations=True,
            )

            return {"status": "success"}

        except Exception as error:
            print(
                f"[CONTACTS FAILED] "
                f"state={contacts['state']} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )

            return {"status": "failed"}


async def main(browser) -> None:
    viewports = get_viewports_by_names(
        SELECTED_VIEWPORTS,
    )

    semaphore = asyncio.Semaphore(
        MAX_CONCURRENT_WORKERS,
    )

    jobs = []

    for state in CONTACT_STATES:
        for sample_index in range(
            NUM_SAMPLES_PER_STATE,
        ):
            contacts = generate_contacts_data(
                state=state,
            )

            for viewport in viewports:
                jobs.append(
                    render_job(
                        browser=browser,
                        semaphore=semaphore,
                        sample_index=sample_index,
                        contacts=contacts,
                        system=generate_system_data(),
                        theme=generate_theme(),
                        viewport=viewport,
                    )
                )

    results = await asyncio.gather(*jobs)

    print(
        f"[GOOGLE CONTACTS COMPLETE] "
        f"successful={sum(x['status'] == 'success' for x in results)} "
        f"failed={sum(x['status'] == 'failed' for x in results)}"
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