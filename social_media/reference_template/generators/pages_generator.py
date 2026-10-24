from __future__ import annotations
import random
from copy import deepcopy

PAGE_STATES = {
 'browserbase': {
  'overview':['populated','empty','date_picker','project_picker'],
  'sessions':['populated','filtered','empty','filter_dialog'],
  'session_replay':['replay','paused','network','session_expired'],
  'agents':['populated','empty','running','create_agent'],
  'agent_run':['complete','running','failed','optimization'],
  'functions':['invocations','failed','empty','deploy_function'],
 },
 'doordash': {
  'dashboard':['overview','announcements','empty','date_picker'],
  'onboarding':['checklist','menu_review','logo_upload','ready'],
  'sales':['overview','orders','empty','create_report'],
  'product_mix':['populated','searched','empty','channel_picker'],
  'cancellations':['overview','categories','empty','date_picker'],
  'orders':['active','scheduled','history','order_details'],
 }
}
POPUPS={'date_picker','project_picker','filter_dialog','session_expired','create_agent','deploy_function','logo_upload','create_report','channel_picker'}
DRAWERS={'optimization','order_details'}

NAV={
 'browserbase':[('overview','Overview','dashboard'),('sessions','Sessions','desktop_windows'),('agents','Agents','smart_toy'),('functions','Functions','functions'),('session_replay','Playground','play_arrow')],
 'doordash':[('dashboard','Home','home'),('sales','Sales','monitoring'),('product_mix','Product mix','bar_chart'),('cancellations','Cancellations','cancel'),('orders','Orders','receipt_long'),('onboarding','Menu','restaurant_menu')]
}

def generate_data(sample_index:int, app:str)->dict:
 rng=random.Random(sample_index+ (1000 if app=='doordash' else 0))
 return {'sample_index':sample_index,'app':app,'nav':NAV[app], 'sessions':[{'id':f'{rng.getrandbits(32):08x}', 'status':'Completed' if i%4 else 'Failed', 'started':f'Aug {3+i}, 10:{10+i}:06 AM','duration':f'00:0{i%3}:{12+i:02d}','region':'us-west-2','expires':f'{i+1} days'} for i in range(8)],'products':[{'name':n,'sales':f'${rng.randint(5,40)}.00','orders':rng.randint(1,9)} for n in ['Green Goddess Bowl','Matcha Latte','Chocolate Bliss','Smoky Chipotle Wrap','Avocado Toast','Iced Coffee','Berry Smoothie','Harvest Salad']], 'agents':[{'name':n,'description':d} for n,d in [('Tech News Summarizer','Summarize the top trending technology articles.'),('Price Monitor','Compare product prices across storefronts.'),('Research Assistant','Collect and organize public research results.')]], 'orders':[{'id':f'{rng.getrandbits(32):08X}','customer':n,'status':'Preparing' if i%2 else 'New','total':f'${18+i*4}.50'} for i,n in enumerate(['Taylor C.','Morgan R.','Jamie L.','Alex P.','Sam W.'])], 'events':[{'kind':k,'text':t,'time':f'0:{i*3:02d}'} for i,(k,t) in enumerate([('Prompt','Summarize the top five technology articles.'),('Reason','Choose a structured source'),('Tool','Fetch API'),('Tool','Parse response'),('Tool','Extract headlines'),('Reason','Verify summaries'),('Tool','Return result')])]}

def apply_state(base:dict,page:str,state:str)->dict:
 if page not in PAGE_STATES[base['app']] or state not in PAGE_STATES[base['app']][page]:raise ValueError((page,state))
 d=deepcopy(base);d.update(page=page,state=state,popup_visible=state in POPUPS or state in DRAWERS, drawer=state in DRAWERS,title=page.replace('_',' ').title(),empty=state=='empty')
 d['dialog_title']={'date_picker':'Select date range','project_picker':'Switch project','filter_dialog':'Filter sessions','session_expired':'Session has expired','create_agent':'Create agent','deploy_function':'Deploy function','logo_upload':'Add your logo','create_report':'Create sales report','channel_picker':'Order channels','optimization':'Optimize agent','order_details':'Order: FC9E32CA'}.get(state,'')
 return d
