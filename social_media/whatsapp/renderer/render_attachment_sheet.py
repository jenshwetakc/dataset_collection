from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.whatsapp.generators.attachment_sheet_generator import (
    generate_attachment_sheet_page,
)
from social_media.whatsapp.generators.chat_generator import (
    generate_system_status,
)
from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)


NUM_SAMPLES = 50

VIEWPORT_MODE = "selected"

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

MAX_CONCURRENT_WORKERS = 4


ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

async def render_attachment_sheet_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    attachment: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[WHATSAPP ATTACHMENT SHEET] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type="attachment_sheet",
                template_name="attachment_sheet.html",
                context_key="attachment",
                page_data=attachment,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="attachment_sheet",
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }
        except Exception as error:
            print(
                f"[WHATSAPP ATTACHMENT SHEET FAILED] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"error={error}"
            )
            return {
                "status": "failed",
                "sample_index": sample_index,
                "viewport": viewport["name"],
                "error": str(error),
            }


async def main(browser) -> None:
    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    jobs = []

    print("\nRendering Attachment Sheet")
    print("Viewports:")

    for viewport in viewports:
        print(
            f"  {viewport['name']} | "
            f"{viewport['category']} | "
            f"{viewport['orientation']} | "
            f"{viewport['size_class']} | "
            f"{viewport['width']}x{viewport['height']} | "
            f"DPR={viewport.get('dpr', 1)}"
        )

    for sample_index in range(1, NUM_SAMPLES + 1):
        print(
            f"\nGenerating sample "
            f"{sample_index}/{NUM_SAMPLES}"
        )

        attachment = generate_attachment_sheet_page()
        system = generate_system_status()

        theme_mode = random.choice(
            ["light", "dark"]
        )
        theme = generate_accessible_theme(
            mode=theme_mode,
        )

        print("Actions:", attachment["action_count"])
        print("Recent media:", attachment["recent_media_count"])
        print(
            "Show recent media:",
            attachment["show_recent_media"],
        )
        print("Show close:", attachment["show_close"])
        print("Theme:", theme_mode)

        for viewport in viewports:
            jobs.append(
                render_attachment_sheet_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    attachment=attachment,
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

    print(
        f"[WHATSAPP ATTACHMENT SHEET COMPLETE] "
        f"successful={successful} "
        f"failed={failed}"
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