from __future__ import annotations
import argparse, asyncio, random, sys
from pathlib import Path
if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from playwright.async_api import async_playwright
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.bbc.generators.shared import STATES, generate_data, apply_state
from social_media.common.all_common import render_page
ROOT=Path(__file__).resolve().parents[1]
NUM_SAMPLES=1
SELECTED_VIEWPORTS=['small_mobile',  'ultrawide']
MAX_CONCURRENT_WORKERS=4
SAVE_VISUALIZATIONS=True
SCROLL_PERCENTAGES=[0,25,50,75,100]
async def run(page_names=None, samples=NUM_SAMPLES, viewport_names=None, assets_dir=None):
    names=page_names or list(STATES)
    viewports=get_viewports_by_names(viewport_names or SELECTED_VIEWPORTS)
    semaphore=asyncio.Semaphore(MAX_CONCURRENT_WORKERS)
    failures=[];successful=0
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True)
        async def job(page,sample,data,theme,vp):
            async with semaphore:
                try:
                    await render_page(browser=browser,sample_index=sample,page_type=f"{page}_{data['state']}",template_name=f'{page}.html',context_key='ff',page_data=data,system=generate_system_data(style='random',icon_density='random',viewport=vp),theme=theme,viewport=vp,template_dir=ROOT/'templates',output_root=ROOT/'output',output_subdir=page,annotation_profiles=['big_components','small_elements'],capture_full_page=False,capture_viewports=True,scroll_percentages=[0] if data['popup_mode'] or data['keyboard_visible'] else SCROLL_PERCENTAGES,save_visualizations=SAVE_VISUALIZATIONS)
                    return True
                except Exception as e:
                    failures.append(f"{page}/{data['state']}/{vp['name']}: {e!r}");print(failures[-1]);return False
        try:
            for page in names:
                for sample in range(samples):
                    base=generate_data(page,sample,assets_dir)
                    theme=generate_accessible_theme(mode=random.choice(['light','dark']))
                    for state in STATES[page]:
                        data=apply_state(base,state)
                        results=await asyncio.gather(*(job(page,sample,data,theme,vp) for vp in viewports))
                        successful+=sum(results)
        finally: await browser.close()
    print(f'Complete: successful={successful}, failed={len(failures)}')
    if failures: raise RuntimeError('\n'.join(failures))
def cli(default_page=None):
    p=argparse.ArgumentParser()
    p.add_argument('--page',choices=list(STATES)+['all'],default=default_page or 'all')
    p.add_argument('--samples',type=int,default=NUM_SAMPLES)
    p.add_argument('--viewports',nargs='+',default=SELECTED_VIEWPORTS)
    p.add_argument('--assets-dir',type=Path)
    a=p.parse_args()
    if a.samples<1:p.error('--samples must be positive')
    asyncio.run(run(None if a.page=='all' else [a.page],a.samples,a.viewports,a.assets_dir))
if __name__=='__main__':cli()
