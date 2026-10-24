from __future__ import annotations

import asyncio
import random
from pathlib import Path

from playwright.async_api import async_playwright

from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.viewport import get_viewports_by_names
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.pinterest.generators.home_generator import HOME_STATES, generate_home_page
from social_media.pinterest.renderers.common_renderer import render_page

PINTEREST_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PINTEREST_ROOT / 'templates'
OUTPUT_ROOT = PINTEREST_ROOT / 'output'

NUM_SAMPLES = 5
VIEWPORTS = [
    'small_mobile',
    # 'standard_android', 'standard_iphone', 'large_mobile',
    # 'mobile_landscape', 'tablet_portrait', 'large_tablet_portrait',
    # 'tablet_landscape', 'foldable', 'small_laptop', 'laptop', 'large_laptop',
    # 'desktop_fhd', 'desktop_qhd', 'desktop_4k',
    'ultrawide',
]
STATES = HOME_STATES
ANNOTATION_PROFILES = ['big_components', 'small_elements']
THEME_MODE = 'random'
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0, 25, 50, 75, 100]
MAX_CONCURRENT_WORKERS = 4
SYSTEM_STYLE = 'random'
ICON_DENSITY = 'random'


def generate_theme() -> dict:
    mode = random.choice(['light', 'dark']) if THEME_MODE == 'random' else THEME_MODE
    return generate_accessible_theme(mode=mode)


async def render_one_home_job(
    browser,
    semaphore: asyncio.Semaphore,
    sample_index: int,
    pinterest: dict,
    system: dict,
    theme: dict,
    viewport: dict,
) -> dict:
    async with semaphore:
        state = pinterest['state']
        metadata = {
            'sample_index': sample_index,
            'state': state,
            'viewport': viewport['name'],
            'theme': theme['mode'],
        }
        try:
            print('[PINTEREST HOME]', metadata)
            await render_page(
                browser=browser,
                sample_index=sample_index,
                page_type=f'pinterest_home_{state}',
                template_name='home.html',
                context_key='pinterest',
                page_data=pinterest,
                system=system,
                theme=theme,
                viewport=viewport,
                template_dir=TEMPLATE_DIR,
                output_root=OUTPUT_ROOT,
                output_subdir='home',
                annotation_profiles=ANNOTATION_PROFILES,
                min_visible_ratio=.20,
                capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS,
                scroll_percentages=[0] if pinterest['popup_visible'] else SCROLL_PERCENTAGES,
                save_visualizations=True,
            )
            return {'status': 'success', **metadata}
        except Exception as error:
            print('[PINTEREST HOME FAILED]', metadata, 'error=', error)
            return {'status': 'failed', **metadata, 'error': str(error)}


async def main(browser) -> None:
    if MAX_CONCURRENT_WORKERS < 1:
        raise ValueError('MAX_CONCURRENT_WORKERS must be at least 1')
    viewports = get_viewports_by_names(VIEWPORTS)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    successful = failed = 0

    # Gather one sample at a time so a large run does not retain thousands
    # of image-heavy page dictionaries and pending tasks in memory.
    for sample_index in range(NUM_SAMPLES):
        seed = random.randrange(2**32)
        data_by_state = {state: generate_home_page(state, seed=seed) for state in STATES}
        theme = generate_theme()
        systems = {
            viewport['name']: generate_system_data(
                style=SYSTEM_STYLE, icon_density=ICON_DENSITY, viewport=viewport,
            )
            for viewport in viewports
        }
        jobs = [
            render_one_home_job(
                browser=browser,
                semaphore=semaphore,
                sample_index=sample_index,
                pinterest=data_by_state[state],
                system=systems[viewport['name']],
                theme=theme,
                viewport=viewport,
            )
            for viewport in viewports
            for state in STATES
        ]
        results = await asyncio.gather(*jobs)
        successful += sum(result['status'] == 'success' for result in results)
        failed += sum(result['status'] == 'failed' for result in results)

    print('\n[PINTEREST HOME COMPLETE]', f'successful={successful}', f'failed={failed}')
    if failed:
        raise RuntimeError(f'{failed} Pinterest renders failed. See the messages above.')


async def run() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            await main(browser)
        finally:
            await browser.close()


if __name__ == '__main__':
    asyncio.run(run())
