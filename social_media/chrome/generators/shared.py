from __future__ import annotations
import copy,random
STATES={'new_tab': ['default', 'shortcuts_hidden', 'custom_background', 'incognito', 'customize', 'add_shortcut'], 'web_page': ['loaded', 'loading', 'offline', 'find', 'browser_menu', 'save_bookmark'], 'tab_manager': ['grid', 'list', 'grouped', 'incognito_tabs', 'tab_search', 'edit_group'], 'history': ['all', 'searched', 'selected', 'empty', 'delete_selected', 'clear_data'], 'downloads': ['completed', 'downloading', 'paused', 'failed', 'blocked', 'remove_download'], 'bookmarks': ['all', 'folder', 'searched', 'empty', 'edit_bookmark', 'new_folder'], 'settings': ['profile', 'appearance', 'privacy', 'search_engine', 'reset_dialog', 'sync_dialog'], 'site_permissions': ['overview', 'camera', 'notifications', 'blocked', 'permission_prompt', 'reset_permissions'], 'extensions': ['installed', 'developer_mode', 'empty', 'disabled', 'extension_details', 'remove_extension'], 'print_preview': ['portrait', 'landscape', 'custom_pages', 'color', 'destination', 'printing']}
POPUPS={'permission_prompt', 'extension_details', 'destination', 'edit_group', 'browser_menu', 'delete_selected', 'clear_data', 'remove_download', 'sync_dialog', 'remove_extension', 'reset_permissions', 'save_bookmark', 'reset_dialog', 'new_folder', 'customize', 'tab_search', 'add_shortcut', 'edit_bookmark'}
def generate_data(page,sample_index=0,assets_dir=None):
 if page not in STATES:raise ValueError(page)
 titles=['Design notes','Mountain travel guide','Weekly reading list','Project dashboard','Recipe collection','Photography tips','Research notebook','City museum','Weather forecast','Team calendar','Learning resources','Music discoveries']
 random.shuffle(titles)
 return {'page':page,'state':STATES[page][0],'popup_visible':False,'query':'design','sample_index':sample_index,'rows':[{'title':t,'url':f'https://example.test/page/{i+1}','time':f'{9+i//6:02d}:{i*5%60:02d}','selected':i<2} for i,t in enumerate(titles)],'files':[{'name':n,'size':s,'url':'https://files.example.test','progress':random.randint(20,75)} for n,s in [('project-notes.pdf','2.4 MB'),('holiday-photos.zip','148 MB'),('research-data.csv','840 KB'),('presentation.pdf','6.2 MB')]],'navigation':list(STATES)}
def apply_state(base,state):
 if state not in STATES[base['page']]:raise ValueError(state)
 d=copy.deepcopy(base);d['state']=state;d['popup_visible']=state in POPUPS
 if state=='searched':d['rows']=[r for r in d['rows'] if 'design' in r['title'].lower()]
 if state=='empty':d['rows']=[]
 return d
