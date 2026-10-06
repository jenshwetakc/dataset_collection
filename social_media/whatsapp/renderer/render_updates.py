import asyncio
import random

from playwright.async_api import (
    async_playwright,
)

from social_media.common.palette_generator import (
    generate_accessible_theme,
)
from social_media.whatsapp.generators.chat_generator import (
    generate_system_status,
)
from social_media.whatsapp.generators.updates_generator import (
    generate_updates_page,
)
from social_media.whatsapp.renderer.common_renderer import (
    render_page,
    resolve_viewports,
)


# ==========================================================
# Configuration
# ==========================================================

NUM_SAMPLES = 50
MAX_CONCURRENT_WORKERS = 4


# ==========================================================
# Viewport Configuration
# ==========================================================

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


async def render_updates_job(
    *,
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    updates: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        try:
            print(
                f"[WHATSAPP UPDATES] "
                f"sample={sample_index} "
                f"viewport={viewport['name']} "
                f"theme={theme['mode']}"
            )

            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type="updates",
                template_name="updates.html",
                context_key="updates",
                page_data=updates,
                system=system,
                theme=theme,
                viewport=viewport,
                output_subdir="updates",
            )

            return {
                "status": "success",
                "sample_index": sample_index,
                "viewport": viewport["name"],
            }

        except Exception as error:
            print(
                f"[WHATSAPP UPDATES FAILED] "
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
    output_index = 1

    print("\nRendering Updates page")
    print("Viewports:")

    for viewport in viewports:
        print(
            f"  {viewport['name']} "
            f"{viewport['width']}x{viewport['height']} "
            f"DPR={viewport.get('dpr', 1)}"
        )

    for sample_number in range(1, NUM_SAMPLES + 1):
        print(f"\nGenerating sample {sample_number}/{NUM_SAMPLES}")

        updates = generate_updates_page()
        system = generate_system_status()

        theme_mode = random.choice(["light", "dark"])
        theme = generate_accessible_theme(mode=theme_mode)

        print("Theme:", theme_mode)

        for viewport in viewports:
            jobs.append(
                render_updates_job(
                    browser=browser,
                    semaphore=semaphore,
                    sample_index=output_index,
                    updates=updates,
                    system=system,
                    theme=theme,
                    viewport=viewport,
                )
            )
            output_index += 1

    results = await asyncio.gather(*jobs)

    successful = sum(
        result["status"] == "success"
        for result in results
    )
    failed = len(results) - successful

    print(
        f"[WHATSAPP UPDATES COMPLETE] "
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