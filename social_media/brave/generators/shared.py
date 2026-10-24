from __future__ import annotations
import copy,random
STATES={'new_tab': ['default', 'private', 'sponsored', 'customize_panel', 'typing', 'restore_session'], 'search_results': ['web', 'images', 'no_results', 'suggestions', 'typing', 'search_settings'], 'web_page': ['loaded', 'advertisement', 'cookie_banner', 'cookie_side', 'permission_panel', 'find_in_page'], 'tab_manager': ['grid', 'list', 'vertical_tabs', 'private_tabs', 'tab_menu', 'close_all'], 'history': ['all', 'searched', 'empty', 'sidebar', 'delete_selected', 'clear_history'], 'bookmarks': ['all', 'folder', 'empty', 'sidebar', 'edit_bookmark', 'new_folder'], 'downloads': ['completed', 'downloading', 'paused', 'failed', 'downloads_panel', 'remove_download'], 'shields': ['standard', 'strict', 'custom', 'tracking_panel', 'site_permissions', 'clear_data'], 'rewards': ['overview', 'enabled', 'disabled', 'statement', 'rewards_panel', 'ad_notification'], 'settings': ['general', 'home', 'search', 'leo_panel', 'password_typing', 'reset_settings']}
MODALS={'reset_settings', 'clear_data', 'edit_bookmark', 'clear_history', 'close_all', 'remove_addon', 'remove_download', 'delete_selected', 'new_folder', 'restore_session'}
PANELS={'customize_panel': 'side_panel', 'search_settings': 'side_panel', 'cookie_side': 'cookie_side', 'sidebar': 'sidebar', 'permission_panel': 'permission', 'suggestions': 'suggestions', 'typing': 'typing', 'tracking_panel': 'tracking', 'downloads_panel': 'downloads', 'cookie_banner': 'cookie_banner', 'find_in_page': 'find', 'tab_menu': 'tab_menu', 'addon_menu': 'addon_menu', 'password_typing': None, 'rewards_panel':'rewards', 'ad_notification':'ad_notification', 'leo_panel':'leo'}
def generate_data(page,sample_index=0,assets_dir=None):
 if page not in STATES:raise ValueError(page)
 titles=['Design notes','Mountain travel guide','Weekly reading list','Project dashboard','Recipe collection','Photography tips','Research notebook','City museum']
 return {'page':page,'state':STATES[page][0],'popup_visible':False,'popup_mode':None,'keyboard_visible':False,'query':'workspace ideas','rows':[{'title':t,'url':f'https://example.test/page/{i+1}','time':f'09:{i*7:02d}','selected':i<2} for i,t in enumerate(titles)],'files':[{'name':n,'size':s,'progress':42} for n,s in [('project-notes.pdf','2.4 MB'),('photos.zip','148 MB'),('research-data.csv','840 KB')]],'sample_index':sample_index}
def apply_state(base,state):
 if state not in STATES[base['page']]:raise ValueError(state)
 d=copy.deepcopy(base);d['state']=state;d['popup_mode']='modal' if state in MODALS else PANELS.get(state);d['popup_visible']=state in MODALS;d['keyboard_visible']=state in {'typing','password_typing'}
 if state in {'empty','no_results'}:d['rows']=[]
 if state=='searched':d['rows']=[r for r in d['rows'] if 'design' in r['title'].lower()]
 return d

PANELS.update({'rewards_panel':'rewards','ad_notification':'ad_notification','leo_panel':'leo'})
