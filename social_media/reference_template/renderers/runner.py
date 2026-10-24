from __future__ import annotations
import argparse
import asyncio
import random
import sys
from pathlib import Path
if __package__ in {None,''}:
 sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from playwright.async_api import async_playwright
from social_media.common.palette_generator import generate_accessible_theme
from social_media.common.dynamic_system_generator import generate_system_data
from social_media.common.viewport import get_viewports_by_names
from social_media.reference_simulators.generators.pages_generator import PAGE_STATES,generate_data,apply_state
from social_media.reference_simulators.renderers.common_renderer import render_page
ROOT=Path(__file__).resolve().parents[1]

async def main(args):
 apps=list(PAGE_STATES) if args.app=='all' else [args.app]
 viewports=get_viewports_by_names(args.viewports)
 failures=[];success=0
 semaphore=asyncio.Semaphore(args.workers)
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True)
  try:
   for app in apps:
    pages=list(PAGE_STATES[app]) if args.page=='all' else [args.page]
    if any(p not in PAGE_STATES[app] for p in pages):raise ValueError(f'Invalid page for {app}: {args.page}')
    for index in range(args.samples):
     base=generate_data(index,app)
     seed='#FF4F00' if app=='browserbase' else '#D92424'
     mode=random.choice(['light','dark']) if args.theme=='random' else args.theme
     theme=generate_accessible_theme(seed=seed,mode=mode)
     for page in pages:
      for state in PAGE_STATES[app][page]:
       data=apply_state(base,page,state)
       async def job(viewport):
        async with semaphore:
         try:
          await render_page(browser=browser,sample_index=index,page_type=f'{app}_{page}_{state}',template_name='workspace.html',context_key='app_data',page_data=data,system=generate_system_data(style='random',viewport=viewport),theme=theme,viewport=viewport,template_dir=ROOT/'templates',output_root=ROOT/'output',output_subdir=f'{app}/{page}',annotation_profiles=['big_components','small_elements'],capture_full_page=args.full_page,capture_viewports=True,scroll_percentages=[0] if data['popup_visible'] else [0,25,50,75,100],save_visualizations=not args.no_visualizations)
          return True
         except Exception as error:
          failures.append((app,page,state,viewport['name'],repr(error)));print('[FAILED]',failures[-1]);return False
       success+=sum(await asyncio.gather(*(job(v) for v in viewports)))
  finally:await browser.close()
 print(f'Completed: successful={success} failed={len(failures)}')
 if failures:raise RuntimeError(f'{len(failures)} jobs failed')

def cli():
 p=argparse.ArgumentParser()
 p.add_argument('--app',choices=['all',*PAGE_STATES],default='all')
 p.add_argument('--page',default='all')
 p.add_argument('--samples',type=int,default=1)
 p.add_argument('--viewports',nargs='+',default=['standard_iphone','laptop','desktop_fhd'])
 p.add_argument('--workers',type=int,default=4)
 p.add_argument('--theme',choices=['light','dark','random'],default='light')
 p.add_argument('--full-page',action='store_true')
 p.add_argument('--no-visualizations',action='store_true')
 a=p.parse_args()
 if a.samples<1 or a.workers<1:p.error('samples and workers must be positive')
 asyncio.run(main(a))
if __name__=='__main__':cli()
