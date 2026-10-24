"""Fictional Medium-style screenshot data, deterministic by seed, Python 3.10+."""
import base64,copy,random
from pathlib import Path
from functools import lru_cache
PAGE_STATES={
'home':['for_you','featured','more_topics','cookie_dialog','save_popover','account_popover'],
'following':['writers','publications','topics','follow_dialog','mute_dialog','cookie_dialog'],
'explore':['recommended','writers','publications','topic_dialog','follow_dialog','search_popover'],
'search':['stories','people','publications','filters_drawer','no_results','search_popover'],
'topic':['latest','best','recommended','follow_dialog','share_dialog','cookie_dialog'],
'story':['full_story','member_preview','highlighted','responses_drawer','share_dialog','report_dialog'],
'profile':['home','lists','about','follow_dialog','subscribe_dialog','profile_popover'],
'publication':['home','latest','about','submission_dialog','subscribe_dialog','cookie_dialog'],
'library':['your_lists','saved_lists','highlights','new_list_dialog','reading_history','delete_dialog'],
'list_detail':['stories','notes','private','edit_list_dialog','share_dialog','save_popover'],
'editor':['draft','formatted','saved','publish_dialog','image_dialog','discard_dialog'],
'stories':['drafts','published','responses','story_popover','delete_dialog','schedule_dialog'],
'stats':['overview','story_detail','audience','date_dialog','export_dialog','cookie_dialog'],
'notifications':['all','responses','followers','notification_popover','preferences_dialog','clear_dialog'],
'membership':['plans','monthly','annual','join_dialog','payment_dialog','gift_dialog'],
'settings':['account','publishing','notifications','password_dialog','cookie_dialog','delete_dialog']}
NAMES=['Alex Morgan','Mira Patel','Jordan Lee','Samira Chen','Noah Rivera','Emma Brooks','Ravi Shah','Lena Park','Amir Costa','Sophie Martin','Theo Williams','Nadia Kim']
TITLES=['The quiet skill of paying attention','What thoughtful technology can learn from ordinary people','A better way to make room for creative work','The small habits that change how we learn','Why cities need more places to pause','Designing software that welcomes everyone','Notes from a year of writing every day','What we lose when everything becomes a metric','A practical guide to asking better questions','The future of work starts with better conversations','How to read a difficult book without giving up','Finding useful ideas outside your own field','The hidden costs of frictionless experiences','A slower approach to building something meaningful','Lessons from an imperfect research notebook','Making sense of uncertainty in a changing world','The overlooked craft of editing your own ideas','When a simple prototype teaches you more than a plan']
TOPICS=['Design','Technology','Writing','Self Improvement','Artificial Intelligence','Science','Productivity','Culture','Programming','Psychology','Books','Creativity']
PUBLICATIONS=['The Thoughtful Observer','Design in Practice','Signals & Stories','Everyday Science','The Writing Room','Human Systems']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=32)
def artwork(i):
 c=['#B4C6B2','#DDC4AA','#B7BDD4','#C6D8D6','#DFC2BD','#D7D0AC'][i%6]
 if i%3==0:shapes='<circle cx="520" cy="100" r="55" fill="#F3E7CA"/><path d="M0 300L120 130 260 300 430 100 640 300V400H0Z" fill="#566F69"/><path d="M0 345Q180 240 370 340T640 320V400H0Z" fill="#8DA698"/>'
 elif i%3==1:shapes='<rect x="90" y="95" width="280" height="200" rx="10" fill="#263A42"/><rect x="105" y="110" width="250" height="165" fill="#DCE9E5"/><path d="M90 295L55 325H405L370 295" fill="#879CA4"/><rect x="455" y="165" width="80" height="155" rx="8" fill="#EFE5D3"/><path d="M495 165Q420 70 475 60Q550 105 495 165" fill="#587D68"/><path d="M495 165Q580 90 560 75Q480 110 495 165" fill="#759B79"/>'
 else:shapes='<rect x="100" y="105" width="145" height="225" rx="5" fill="#315B62"/><rect x="255" y="75" width="145" height="255" rx="5" fill="#C57E5A"/><rect x="410" y="125" width="130" height="205" rx="5" fill="#EEE5CF"/><path d="M120 145H225M120 165H225M275 125H380M275 145H380M430 165H520M430 185H520" stroke="#F6F0E3" stroke-width="5"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400"><rect width="640" height="400" fill="'+c+'"/>'+shapes+'</svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);shift=rng.randrange(len(TITLES));people=[dict(id=i,name=n,initials=''.join(w[0] for w in n.split()),bio=['Writing about the intersection of design, technology, and everyday life.','Researcher, reader, and collector of useful questions.','Independent writer exploring culture and creative practice.'][i%3],followers=1200+i*670) for i,n in enumerate(NAMES)]
 pool=[]
 if media_dir:pool=sorted(p for p in (Path(media_dir)/'stories').glob('*') if p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'})
 stories=[]
 for i in range(18):
  image=artwork(i)
  if pool:
   p=pool[(sample_index+i)%len(pool)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];image='data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  stories.append(dict(id=i,title=TITLES[(i+shift)%len(TITLES)],subtitle=['A few practical observations on making more deliberate choices.','Small experiments, useful questions, and a different perspective.','What everyday experience can teach us about meaningful change.'][i%3],author=people[i%12],publication=PUBLICATIONS[i%6],topic=TOPICS[i%12],image=image,date=['Oct 12','Oct 10','Oct 8','Oct 5'][i%4],minutes=4+i%9,claps=143+i*79,responses=3+i*2,member=i%3!=0,views=1840+i*1120,reads=642+i*470))
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,stories=stories,people=people,topics=TOPICS,publications=PUBLICATIONS,query='thoughtful design',profile=people[0],tab_labels=['Medium — '+page.replace('_',' ').title(),'The quiet skill of paying attention','Your reading list'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith(('_dialog','_drawer','_popover')))
 d['dialog_title']={'cookie_dialog':'Your privacy choices','save_popover':'Save to a list','account_popover':'Your account','follow_dialog':'Discover more voices','mute_dialog':'Mute this writer?','topic_dialog':'Explore your interests','search_popover':'Search Medium','filters_drawer':'Refine your search','responses_drawer':'Responses','share_dialog':'Share this story','report_dialog':'Report this content','subscribe_dialog':'Get new stories by email','profile_popover':'About this writer','submission_dialog':'Submit to this publication','new_list_dialog':'Create a new list','delete_dialog':'Confirm deletion','edit_list_dialog':'Edit list details','publish_dialog':'Ready to publish?','image_dialog':'Add an image','discard_dialog':'Discard changes?','story_popover':'Story options','schedule_dialog':'Schedule your story','date_dialog':'Choose a date range','export_dialog':'Export your stats','notification_popover':'Notification options','preferences_dialog':'Notification preferences','clear_dialog':'Clear notifications?','join_dialog':'Join Medium','payment_dialog':'Payment details','gift_dialog':'Give the gift of reading','password_dialog':'Change password'}.get(state,'Details')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';text='#EBEBE8' if dark else '#242424';surface='#202020' if dark else '#FFFFFF'
 return dict(mode=mode,semantic={'background':'#171717' if dark else '#FFFFFF','on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#30342F' if dark else '#F2F2EF','on_surface_variant':text,'primary':'#8BCE85' if dark else '#1A7C20','on_primary':'#10200E' if dark else '#FFFFFF','border':'#74746E' if dark else '#D7D7D2','icon':text,'error':'#FFB3AE' if dark else '#AC3028'})
