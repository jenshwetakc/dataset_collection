from __future__ import annotations
import asyncio, random
from playwright.async_api import async_playwright
from social_media.google_docs.generators.drive_generator import generate_drive_page
from social_media.google_docs.renderers.common_renderer import render_google_docs_page
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names

NUM_SAMPLES = 25
SELECTED_VIEWPORTS = ["standard_iphone", "laptop", ]
ANNOTATION_PROFILES = ["big_components", "small_elements"]
THEME_MODE = "random"
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SAVE_VISUALIZATIONS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
MAX_CONCURRENT_WORKERS = 4

def generate_theme():
    return generate_accessible_theme(
        mode=random.choice(["light", "dark"]) if THEME_MODE == "random" else THEME_MODE
    )

async def render_job(browser, semaphore, sample_index, drive, system, theme, viewport):
    async with semaphore:
        try:
            await render_google_docs_page(
                browser=browser, sample_index=sample_index, page_type="drive",
                template_name="drive.html", context_key="drive", page_data=drive,
                system=system, theme=theme, viewport=viewport, output_subdir="drive",
                annotation_profiles=ANNOTATION_PROFILES,
                capture_full_page=CAPTURE_FULL_PAGE, capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=SCROLL_PERCENTAGES,
                save_visualizations=SAVE_VISUALIZATIONS,
            )
            return True
        except Exception as error:
            print(f"[DRIVE FAILED] sample={sample_index} viewport={viewport['name']} {error}")
            return False

async def run():
    viewports = get_viewports_by_names(SELECTED_VIEWPORTS)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
            jobs = []
            for sample_index in range(NUM_SAMPLES):
                drive, system, theme = generate_drive_page(), generate_system_data(), generate_theme()
                print(f"[DRIVE] sample={sample_index} state={drive['state']} theme={theme['mode']}")
                for viewport in viewports:
                    jobs.append(render_job(browser, semaphore, sample_index, drive, system, theme, viewport))
            results = await asyncio.gather(*jobs)
            print(f"[DRIVE COMPLETE] successful={sum(results)} failed={len(results)-sum(results)}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())