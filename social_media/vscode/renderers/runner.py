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
from social_media.vscode.generators.pages_generator import PAGE_STATES,generate_data,apply_state,reference_theme
from social_media.common.all_common import render_page
ROOT=Path(__file__).resolve().parents[1]

async def main(args):
 apps=['vscode']
 viewports=get_viewports_by_names(args.viewports)
 failures=[];success=0
 semaphore=asyncio.Semaphore(args.workers)
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(headless=True)
  try:
   for app in apps:
    pages=list(PAGE_STATES) if args.page=='all' else [args.page]
    if any(p not in PAGE_STATES for p in pages):raise ValueError(f'Invalid page for {app}: {args.page}')
    for index in range(args.samples):
     for page in pages:
      base=generate_data(index,page)
      mode='dark' if args.theme=='reference' else random.choice(['light','dark']) if args.theme=='random' else args.theme
      theme=reference_theme(mode) if args.theme=='reference' else generate_accessible_theme(seed='#0078D4',mode=mode)
      states=args.states or PAGE_STATES[page]
      if any(state not in PAGE_STATES[page] for state in states):raise ValueError(f'Unsupported state for {page}: {states}')
      for state in states:
       data=apply_state(base,state)
       async def job(viewport):
        async with semaphore:
         try:
          await render_page(browser=browser,sample_index=index,page_type=f'{app}_{page}_{state}',template_name='workbench.html',context_key='app_data',page_data=data,system=generate_system_data(style='random',viewport=viewport),theme=theme,viewport=viewport,template_dir=ROOT/'templates',output_root=ROOT/'output',output_subdir=page,annotation_profiles=['big_components','small_elements'],capture_full_page=args.full_page,capture_viewports=True,scroll_percentages=[0],save_visualizations=not args.no_visualizations)
          return True
         except Exception as error:
          failures.append((app,page,state,viewport['name'],repr(error)));print('[FAILED]',failures[-1]);return False
       success+=sum(await asyncio.gather(*(job(v) for v in viewports)))
  finally:await browser.close()
 print(f'Completed: successful={success} failed={len(failures)}')
 if failures:raise RuntimeError(f'{len(failures)} jobs failed')

def cli():
 p=argparse.ArgumentParser()
 p.add_argument('--page',default='all')
 p.add_argument('--states',nargs='+',help='Render only these states; use with --page')
 p.add_argument('--samples',type=int,default=1)
 p.add_argument('--viewports',nargs='+',default=['small_mobile','ultrawide'])
 p.add_argument('--workers',type=int,default=4)
 p.add_argument('--theme',choices=['reference','light','dark','random'],default='reference')
 p.add_argument('--full-page',action='store_true')
 p.add_argument('--no-visualizations',action='store_true')
 a=p.parse_args()
 if a.samples<1 or a.workers<1:p.error('samples and workers must be positive')
 asyncio.run(main(a))
if __name__=='__main__':cli()
