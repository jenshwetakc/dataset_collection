from __future__ import annotations

import asyncio
import random

from playwright.async_api import async_playwright

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.whatsapp.generators.chat_generator import (
    generate_system_status,
)
from social_media.whatsapp.generators.new_chat_generator import (
    generate_new_chat_page,
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


async def render_new_chat_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    new_chat: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[WHATSAPP NEW CHAT] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type="new_chat",
                template_name="new_chat.html",
                context_key="new_chat",
                page_data=new_chat,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="new_chat",
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }
        except Exception as error:
            print(
                f"[WHATSAPP NEW CHAT FAILED] "
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

    print("\nRendering New Chat page")
    print("Viewports:")

    for viewport in viewports:
        print(
            f"  {viewport['name']} | "
            f"{viewport['width']}x{viewport['height']} | "
            f"DPR={viewport.get('dpr', 1)}"
        )

    for sample_index in range(1, NUM_SAMPLES + 1):
        print(
            f"\nGenerating sample "
            f"{sample_index}/{NUM_SAMPLES}"
        )

        new_chat = generate_new_chat_page()
        system = generate_system_status()

        theme_mode = random.choice(
            ["light", "dark"]
        )
        theme = generate_accessible_theme(
            mode=theme_mode,
        )

        print("Theme:", theme_mode)
        print("Contacts:", new_chat["contact_count"])
        print("Total contacts:", new_chat["all_contact_count"])
        print("Groups:", len(new_chat["groups"]))
        print("Actions:", len(new_chat["actions"]))
        print("Search active:", new_chat["search"]["active"])
        print("Search query:", new_chat["search"]["query"])

        for viewport in viewports:
            jobs.append(
                render_new_chat_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=sample_index,
                    new_chat=new_chat,
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
        f"[WHATSAPP NEW CHAT COMPLETE] "
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