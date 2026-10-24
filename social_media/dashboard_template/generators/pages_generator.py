from __future__ import annotations
import copy
import random

PAGE_STATES = {
 'visitor_analytics': ['overview','live_traffic','empty','date_picker'],
 'saas_revenue': ['overview','customers','trial_warning','export_report'],
 'team_automation': ['organization','teams','quota_warning','create_scenario'],
 'basketball': ['player_profile','team_stats','game_live','player_details'],
 'personal_banking': ['overview','transactions','payment_failed','send_money'],
 'dental_care': ['landing','services','appointment_success','book_appointment'],
 'crypto_trading': ['overview','portfolio','market_down','buy_crypto'],
 'workflow_editor': ['canvas','running','node_error','configure_node'],
 'business_finance': ['overview','invoices','overdue','create_invoice'],
 'sales_analytics': ['overview','products','target_reached','filter_dialog'],
}
CONFIG = {
 'visitor_analytics': ('MoodyFlow','Visitor analytics','#EF754A','light','0'),
 'saas_revenue': ('Nexus','Revenue overview','#7062E9','light','1'),
 'team_automation': ('Orbit','Managing your team and workflows','#778A10','light','2'),
 'basketball': ('CourtSide','Player performance','#7946DA','dark','3'),
 'personal_banking': ('FlowBank','Good morning, Sarah','#7062E9','light','4'),
 'dental_care': ('Denta','Modern care for a perfect smile','#B13D00','dark','5'),
 'crypto_trading': ('Vault','Market overview','#178766','dark','6'),
 'workflow_editor': ('MakeFlow','Customer onboarding flow','#418276','light','7'),
 'business_finance': ('Chaui','Financial dashboard','#4381BB','light','8'),
 'sales_analytics': ('Ledger','Sales dashboard','#EC7447','light','9'),
}
MODALS={'date_picker','export_report','create_scenario','send_money','book_appointment','buy_crypto','create_invoice','filter_dialog'}
DRAWERS={'player_details','configure_node'}

def generate_data(sample_index: int=0, page: str='visitor_analytics') -> dict:
 if page not in PAGE_STATES: raise ValueError(f'Unknown dashboard: {page}')
 rng=random.Random(f'{page}:{sample_index}')
 brand,title,seed,mode,ref=CONFIG[page]
 names=['Alex Morgan','Sam Rivera','Jamie Park','Taylor Chen','Casey Reed','Jordan Patel','Riley Kim','Drew Lopez']
 rows=[{'id':f'TX-{1000+sample_index*20+i}','name':n,'initials':''.join(x[0] for x in n.split()),'amount':f'{rng.randint(80,4800):,}.00','date':f'Oct {7-i}, 2026','status':rng.choice(['Paid','Pending','Completed']), 'volume':rng.randint(15,250),'email':n.lower().replace(' ','.')+'@example.com'} for i,n in enumerate(names)]
 return {'page':page,'brand':brand,'title':title,'seed':seed,'preferred_mode':mode,'reference_index':ref,'sample_index':sample_index,'rows':rows,'values':[rng.randint(20,95) for _ in range(12)],'balance':f'{rng.randint(22000,40000):,}.00','revenue':f'{rng.randint(40000,75000):,}.00','popup_visible':False,'drawer':False,'state':'overview','empty':False,'active_tab':0,'warning':False,'success':False,'running':False,'dialog_title':''}

def apply_state(base:dict,state:str)->dict:
 data=copy.deepcopy(base);page=data['page']
 if state not in PAGE_STATES[page]:raise ValueError(f'Unsupported state {state} for {page}')
 data.update(state=state,popup_visible=state in MODALS|DRAWERS,drawer=state in DRAWERS,empty=state=='empty',active_tab=1 if state in {'customers','teams','team_stats','transactions','services','portfolio','invoices','products'} else 0,warning=state in {'trial_warning','quota_warning','payment_failed','market_down','node_error','overdue'},success=state in {'appointment_success','target_reached'},running=state in {'live_traffic','game_live','running'})
 data['dialog_title']={'date_picker':'Choose date range','export_report':'Export revenue report','create_scenario':'Create a new scenario','player_details':'Marcus Huntington','send_money':'Send money','book_appointment':'Book an appointment','buy_crypto':'Buy Bitcoin','configure_node':'Configure customer record','create_invoice':'Create an invoice','filter_dialog':'Filter sales data'}.get(state,'')
 if state=='overdue':
  for row in data['rows'][::2]:row['status']='Overdue'
 if state=='payment_failed':data['rows'][0]['status']='Failed'
 if page=='crypto_trading' and state=='portfolio':
  for row,name in zip(data['rows'],['Bitcoin','Ethereum','Solana','Polygon','Avalanche','Chainlink','USD Coin','Arbitrum']):
   row.update(name=name,initials=name[:2].upper(),email='Digital asset holding',status='Held')
 if page=='sales_analytics' and state=='products':
  for row,name in zip(data['rows'],['Design subscription','Premium workspace','Analytics package','Starter plan','Team bundle','Cloud storage','Support package','Enterprise plan']):
   row.update(name=name,initials=name[:2].upper(),email='Monthly subscription',status='Active')
 return data
