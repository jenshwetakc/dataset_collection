from __future__ import annotations
import copy
import random
import base64
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def font_uri():
 path=Path(__file__).resolve().parents[1]/"assets"/"material-symbols-rounded.woff2"
 return "data:font/woff2;base64,"+base64.b64encode(path.read_bytes()).decode("ascii")

PAGE_STATES={
 'welcome':['recent','empty','walkthrough','workspace_trust'],
 'editor':['editing','split','unsaved','find_widget'],
 'search':['results','replace','no_results','replace_confirm'],
 'source_control':['changes','staged','clean','commit_dialog'],
 'debug':['launch','paused','running','breakpoint_dialog'],
 'extensions':['marketplace','installed','installing','extension_details'],
 'terminal':['shell','build','problems','task_picker'],
 'settings':['user','workspace','modified','reset_dialog'],
 'notebook':['ready','executed','cell_error','kernel_picker'],
 'diff':['modified','inline','merge_conflict','resolve_dialog'],
}
MODALS={'workspace_trust','replace_confirm','commit_dialog','breakpoint_dialog','task_picker','reset_dialog','kernel_picker','resolve_dialog'}
TITLES={'welcome':'Welcome','editor':'app.ts','search':'Search','source_control':'Source Control','debug':'Run and Debug','extensions':'Extensions','terminal':'Terminal','settings':'Settings','notebook':'analysis.ipynb','diff':'app.ts (Working Tree)'}
CODE=[('comment','// Northstar workspace — application entry point'),('keyword',"import { createServer } from './server';"),('keyword',"import { loadConfig } from './config';"),('plain',''),('keyword','interface ApplicationConfig {'),('plain','  port: number;'),('plain','  environment: string;'),('plain','}'),('plain',''),('keyword','export async function startApplication() {'),('plain','  const config = loadConfig();'),('plain','  const server = createServer(config);'),('plain',''),('comment','  // Connect services before accepting requests'),('plain','  await server.connect();'),('plain','  await server.listen(config.port);'),('plain',''),('string',"  console.log(`Ready on port ${config.port}`);"),('plain','  return server;'),('plain','}'),('plain',''),('keyword','startApplication().catch((error) => {'),('plain','  console.error(error);'),('plain','  process.exit(1);'),('plain','});')]
EXTENSIONS=[('Python','Microsoft','Python language support, debugging, and environments.','48.2M','4.7','code'),('Pylance','Microsoft','Fast, feature-rich language support for Python.','39.4M','4.6','bolt'),('ESLint','Microsoft','Integrates ESLint JavaScript into the editor.','34.8M','4.5','check_circle'),('Prettier','Prettier','Code formatter for JavaScript, TypeScript, and more.','51.1M','4.8','format_align_left'),('GitLens','GitKraken','Explore your repositories and understand your code.','28.7M','4.6','account_tree'),('Jupyter','Microsoft','Interactive notebooks and data science tools.','27.5M','4.7','science')]

def generate_data(sample_index:int=0,page:str='welcome')->dict:
 if page not in PAGE_STATES:raise ValueError(f'Unknown VS Code view: {page}')
 rng=random.Random(f'vscode:{page}:{sample_index}')
 return dict(page=page,title=TITLES[page],sample_index=sample_index,state=PAGE_STATES[page][0],popup_visible=False,font_uri=font_uri(),workspace='northstar-app',branch='feature/dashboard',code=copy.deepcopy(CODE),files=['app.ts','server.ts','config.ts','components','Dashboard.tsx','Button.tsx','styles.css','package.json','README.md'],recent=['northstar-app','data-tools','portfolio-web'],extensions=copy.deepcopy(EXTENSIONS),query='createServer',matches=12+rng.randint(0,4),dialog_title='')

def apply_state(base:dict,state:str)->dict:
 d=copy.deepcopy(base)
 if state not in PAGE_STATES[d['page']]:raise ValueError(f'Invalid state {state} for {d["page"]}')
 d.update(state=state,popup_visible=state in MODALS)
 d['dialog_title']={'workspace_trust':'Do you trust the authors of the files in this folder?','replace_confirm':'Replace all matching occurrences?','commit_dialog':'Commit changes','breakpoint_dialog':'Edit breakpoint','task_picker':'Select the task to run','reset_dialog':'Reset modified settings?','kernel_picker':'Select a notebook kernel','resolve_dialog':'Complete merge'}.get(state,'')
 return d

def reference_theme(mode='dark')->dict:
 if mode not in {'light','dark'}:raise ValueError(mode)
 dark=mode=='dark';bg='#1F1F1F' if dark else '#FFFFFF';surface='#181818' if dark else '#F3F3F3';fg='#CCCCCC' if dark else '#242424';border='#454545' if dark else '#C8C8C8'
 return {'mode':mode,'semantic':{'background':bg,'surface':surface,'on_background':fg,'on_surface':fg,'primary':'#0078D4','on_primary':'#FFFFFF','border':border,'border_subtle':'#2B2B2B' if dark else '#DEDEDE','icon':fg,'surface_variant':'#2A2D2E' if dark else '#E8E8E8','on_surface_variant':'#AFAFAF' if dark else '#555555'}}
