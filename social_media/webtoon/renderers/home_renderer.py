from __future__ import annotations
import asyncio
import importlib
import random
from playwright.async_api import async_playwright
from social_media.webtoon.generators.home_generator import STATES, generate_home_page, make_state
from social_media.webtoon.renderers.common_renderer import render_webtoon_page

PACKAGE_ROOT = __package__.split('.')[0]
NUM_SAMPLES = 5
VIEWPORTS = ['small_mobile',
             # 'standard_android','standard_iphone','large_mobile','mobile_landscape','tablet_portrait','large_tablet_portrait','tablet_landscape','foldable','small_laptop','laptop','large_laptop','desktop_fhd','desktop_qhd','desktop_4k',
             'ultrawide']
ANNOTATION_PROFILES = ['big_components','small_elements']
THEME_MODE = 'random'
CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True
SCROLL_PERCENTAGES = [0,25,50,75,100]
MAX_CONCURRENT_WORKERS = 4
SAVE_VISUALIZATIONS = True
SYSTEM_STYLE = 'random'
ICON_DENSITY = 'random'
PAGE_STATES = list(STATES)

async def render_one_job(browser, semaphore, sample_index, data, system, theme, viewport):
    async with semaphore:
        try:
            await render_webtoon_page(browser=browser, sample_index=sample_index,
                page_type=f"webtoon_home_{data['state']}", template_name='home.html', context_key='webtoon',
                page_data=data, system=system, theme=theme, viewport=viewport, output_subdir='home',
                annotation_profiles=ANNOTATION_PROFILES, capture_full_page=CAPTURE_FULL_PAGE,
                capture_viewports=CAPTURE_VIEWPORTS, scroll_percentages=SCROLL_PERCENTAGES,
                save_visualizations=SAVE_VISUALIZATIONS)
            print(f"[WEBTOON home OK] sample={sample_index} state={data['state']} viewport={viewport['name']}")
            return True
        except Exception as exc:
            print(f"[WEBTOON home FAILED] sample={sample_index} state={data['state']} viewport={viewport['name']} error={exc!r}")
            return False

async def main(browser):
    palette = importlib.import_module(f'{PACKAGE_ROOT}.common.palette_generator')
    viewport_module = importlib.import_module(f'{PACKAGE_ROOT}.common.viewport')
    dynamic = importlib.import_module(f'{PACKAGE_ROOT}.common.dynamic_system_generator')
    viewports = viewport_module.get_viewports_by_names(VIEWPORTS)
    if not viewports or MAX_CONCURRENT_WORKERS < 1:
        raise ValueError('Resolve at least one viewport and use at least one worker.')
    if THEME_MODE not in {'random','light','dark'}:
        raise ValueError('THEME_MODE must be random, light or dark.')
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    total_ok = total_failed = 0
    for sample_index in range(NUM_SAMPLES):
        content = generate_home_page(package_root=PACKAGE_ROOT)
        theme = palette.generate_accessible_theme(mode=random.choice(['light','dark']) if THEME_MODE=='random' else THEME_MODE)
        state_data = [make_state(content,state) for state in PAGE_STATES]
        jobs = []
        for viewport in viewports:
            system = dynamic.generate_system_data(style=SYSTEM_STYLE,icon_density=ICON_DENSITY,viewport=viewport)
            for data in state_data:
                jobs.append(render_one_job(browser,semaphore,sample_index,data,system,theme,viewport))
        results = await asyncio.gather(*jobs)
        ok = sum(results); failed = len(results)-ok
        total_ok += ok; total_failed += failed
        print(f'[WEBTOON SAMPLE COMPLETE] sample={sample_index} successful={ok} failed={failed}')
    print(f'[WEBTOON home COMPLETE] successful={total_ok} failed={total_failed}')
    if total_failed:
        raise RuntimeError(f'{total_failed} render jobs failed; see errors above.')

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            await main(browser)
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
