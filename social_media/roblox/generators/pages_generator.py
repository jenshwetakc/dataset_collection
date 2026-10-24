"""Fictional Roblox-style screenshot scenarios; Python 3.10+."""
import base64,copy,random
from functools import lru_cache
from pathlib import Path
PAGE_STATES={
'home':['for_you','continue','connections','cookie_dialog','announcements_drawer','account_popover'],
'charts':['trending','top_rated','popular','filters_drawer','genre_dialog','cookie_dialog'],
'search':['experiences','people','items','filters_drawer','no_results','search_popover'],
'experience':['about','servers','passes','join_dialog','favorite_dialog','report_dialog'],
'marketplace':['recommended','accessories','clothing','filters_drawer','cart_drawer','cookie_dialog'],
'item_detail':['overview','try_on','resale','purchase_dialog','outfit_dialog','report_dialog'],
'avatar':['customize','clothing','animations','outfit_dialog','reset_dialog','body_dialog'],
'profile':['about','creations','favorites','message_dialog','connection_dialog','report_dialog'],
'connections':['connections','requests','following','invite_dialog','remove_dialog','profile_popover'],
'communities':['discover','joined','managed','create_dialog','join_dialog','cookie_dialog'],
'community_detail':['overview','store','members','join_dialog','announcement_dialog','report_dialog'],
'inventory':['accessories','clothing','passes','item_dialog','delete_dialog','filters_drawer'],
'messages':['inbox','conversation','archived','compose_dialog','attachment_dialog','delete_dialog'],
'notifications':['all','social','updates','preferences_dialog','notification_popover','clear_dialog'],
'robux':['packages','subscription','gift','redeem_dialog','purchase_dialog','cookie_dialog'],
'transactions':['summary','purchases','sales','date_dialog','export_dialog','details_dialog'],
'settings':['account','privacy','notifications','password_dialog','cookie_dialog','delete_dialog'],
'creator_dashboard':['overview','experiences','analytics','create_dialog','publish_dialog','collaborate_dialog'],
'events':['discover','event_detail','past','reminder_dialog','share_dialog','cookie_dialog'],
'game_session':['playing','paused','scoreboard','settings_dialog','leave_dialog','report_dialog']}
GAME_NAMES=['Skyline Builders','Crystal Cavern Quest','Coastal City Stories','Cloud Parkour','Forest Friends','Turbo Track Racers','Lunar Base Tycoon','Puzzle Planet','Tiny Town Adventures','Island Explorers','Snowy Summit Escape','Robot Workshop','Garden Growers','Mystery Station','Starship Crew','Pixel Pet Village','Festival Park','Ocean Odyssey','Castle Crafters','Desert Rally','Neon Skate Plaza','Mountain Rescue','Dreamhouse Design','Space Academy']
ITEM_NAMES=['Explorer Backpack','Cloud Cap','Pixel Headphones','Midnight Jacket','Sunset Sneakers','Forest Scarf','Orbit Helmet','Retro Shades','Blue Hoodie','Adventure Boots','Neon Visor','Star Shoulder Buddy','Canvas Satchel','Comet Hair','Classic Shirt','Ocean Wings','City Beanie','Festival Top','Builder Belt','Crystal Crown','Lunar Suit','Garden Hat','Sporty Hair','Robot Mask']
NAMES=['PixelTrail','NovaBuilder','CloudRider','MiraMakes','OrbitScout','SkylineSam','LunarLena','CraftyKai','OceanAsh','GardenJay','TurboTheo','PuzzledPiper']
GENRES=['Adventure','Simulation','Roleplay','Obby','Racing','Puzzle','Survival','Social']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=120)
def art(kind,i):
 colors=['#709DCF','#967AC6','#6CA98A','#D29E5E','#B8718E','#718BC2'];c=colors[i%6]
 if kind=='world':
  shapes='<circle cx="510" cy="80" r="45" fill="#F4E6AD"/><path d="M0 260L100 120 230 260 400 80 640 280V400H0Z" fill="#4A7774"/><path d="M0 310L640 240V400H0Z" fill="#76A765"/><path d="M290 400L370 400 440 250 400 240Z" fill="#E3C39A"/><g stroke="#263F50" stroke-width="3"><path d="M90 220V130l70-30 70 35v95l-65 28Z" fill="'+c+'"/><path d="m90 130 75 35 65-30M165 165v93" fill="none"/><rect x="440" y="165" width="90" height="120" fill="#DBC597"/><path d="m430 165 55-55 55 55Z" fill="#925E68"/></g><g fill="#D7E7EC"><rect x="110" y="165" width="22" height="30"/><rect x="180" y="180" width="25" height="30"/><rect x="460" y="190" width="20" height="25"/></g>'
  if i%4==1:
   shapes='<path d="M0 270L640 240V400H0Z" fill="#81899A"/><path d="M230 400L300 170H370L480 400Z" fill="#303E53"/><path d="M350 190L360 230M370 260L390 300M405 335L430 390" stroke="#F8E5A0" stroke-width="9"/><path d="M50 260V110H140V260M500 250V80H590V250" fill="'+c+'"/><rect x="295" y="265" width="90" height="55" rx="12" fill="#ECAC57"/><rect x="310" y="275" width="55" height="20" fill="#35495B"/><circle cx="310" cy="320" r="13" fill="#263140"/><circle cx="370" cy="320" r="13" fill="#263140"/>'
  elif i%4==2:
   shapes='<circle cx="510" cy="90" r="45" fill="#F0E2BC"/><path d="m70 265 115-40 100 40-100 45Z" fill="#B5D184"/><path d="m70 265 115 95 100-95-100 45Z" fill="#8373A1"/><path d="m335 145 85-35 95 35-95 35Z" fill="#B5D184"/><path d="m335 145 85 95 95-95-95 35Z" fill="#8373A1"/><path d="m265 220 55-20 55 20-55 20Z" fill="#E5C889"/><rect x="400" y="35" width="45" height="105" fill="'+c+'"/><path d="m385 35 40-30 35 30Z" fill="#AE778E"/><g fill="#F8E6AE"><circle cx="80" cy="70" r="7"/><circle cx="255" cy="110" r="6"/><circle cx="555" cy="265" r="8"/></g>'
  elif i%4==3:
   shapes='<path d="M0 280L170 90 320 285 480 125 640 280V400H0Z" fill="#568573"/><path d="M0 310Q220 230 410 310T640 300V400H0Z" fill="#8AB281"/><ellipse cx="390" cy="340" rx="160" ry="45" fill="#76B6CC"/><g fill="#326D5D"><path d="m50 240 65-150 65 150ZM160 280l55-160 55 160ZM440 220l60-155 60 155Z"/></g><g fill="#6E594A"><rect x="105" y="230" width="20" height="90"/><rect x="205" y="270" width="20" height="70"/><rect x="490" y="210" width="20" height="80"/></g><path d="M285 280h70v65h-70Z" fill="'+c+'"/><path d="m270 280 50-50 50 50Z" fill="#A87861"/>'
 elif kind=='avatar':
  shapes='<ellipse cx="320" cy="360" rx="100" ry="20" fill="#0002"/><rect x="270" y="65" width="100" height="90" rx="12" fill="#E7BD8A"/><path d="M265 90V60l55-20 55 20v35l-30-20-35 20Z" fill="#3A3C47"/><rect x="245" y="160" width="150" height="125" rx="9" fill="'+c+'"/><rect x="195" y="165" width="45" height="130" rx="8" fill="#E7BD8A"/><rect x="400" y="165" width="45" height="130" rx="8" fill="#E7BD8A"/><rect x="250" y="290" width="65" height="90" rx="7" fill="#344557"/><rect x="325" y="290" width="65" height="90" rx="7" fill="#344557"/><circle cx="300" cy="110" r="5" fill="#36333A"/><circle cx="340" cy="110" r="5" fill="#36333A"/><path d="M300 130q20 15 40 0" fill="none" stroke="#36333A" stroke-width="4"/>'
 else:
  if i%4==0:shapes='<rect x="205" y="120" width="230" height="230" rx="35" fill="'+c+'"/><path d="M250 125V90q70-70 140 0v35" fill="none" stroke="#3E4A5B" stroke-width="25"/><rect x="235" y="220" width="170" height="100" rx="18" fill="#344658"/><path d="M250 170h140M260 240h120" stroke="#DDE7EC" stroke-width="9"/>'
  elif i%4==1:shapes='<path d="M180 230q0-150 150-150t150 150Z" fill="'+c+'"/><path d="M170 230h310q80 10 20 45H170Z" fill="#334656"/><path d="M330 85v140" stroke="#DDE7EC" stroke-width="7"/>'
  elif i%4==2:shapes='<path d="M190 235V170q0-105 130-105t130 105v65" fill="none" stroke="'+c+'" stroke-width="35"/><rect x="170" y="190" width="75" height="130" rx="22" fill="#38475C"/><rect x="395" y="190" width="75" height="130" rx="22" fill="#38475C"/>'
  else:shapes='<path d="m240 80 80 30 80-30 90 80-60 70-35-30v160H245V200l-35 30-60-70Z" fill="'+c+'"/><path d="M320 110v245M250 230h140" stroke="#E1E8EE" stroke-width="8"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400"><rect width="640" height="400" fill="'+('#BFD5DE' if kind=='world' else '#D9DEE4')+'"/>'+shapes+'</svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);shift=rng.randrange(24)
 def image(kind,i):
  if media_dir:
   files=sorted(p for p in (Path(media_dir)/kind).glob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
   if files:
    p=files[(sample_index+i)%len(files)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];return 'data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  return art(kind,i)
 people=[dict(id=i,name=n,initials=n[:2],image=image('avatar',i),online=i%3!=0,followers=180+i*43,status=['In an experience','Online','Offline'][i%3]) for i,n in enumerate(NAMES)]
 games=[dict(id=i,title=GAME_NAMES[(i+shift)%24],image=image('world',i),creator=people[i%12]['name'],genre=GENRES[i%8],rating=88+i%11,players=str(12+i*3)+'.'+str(i%9)+'K',visits=str(2+i*4)+'.5M',favorites=1240+i*150) for i in range(24)]
 items=[dict(id=i,name=ITEM_NAMES[(i+shift)%24],image=image('item',i),price=25+i*15,creator=people[i%12]['name'],category=['Accessories','Clothing','Heads','Animations'][i%4]) for i in range(24)]
 groups=[dict(id=i,name=n,members=4500+i*2700,image=image('world',i+3),description='A fictional community for creative builders, friendly challenges, and sharing new experiences.') for i,n in enumerate(['Skyline Creators','Cloud Adventure Club','Pixel Workshop','Coastal Explorers','Garden Makers','Lunar Academy','Puzzle Collective','Turbo Track Team'])]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,games=games,items=items,people=people,groups=groups,genres=GENRES,profile=people[0],query='adventure',balance=1250,tab_labels=['Roblox — '+page.replace('_',' ').title(),'Skyline Builders','Marketplace'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith(('_dialog','_drawer','_popover')) or (data['page']=='game_session' and state=='paused'))
 d['dialog_title']={'paused':'Paused','cookie_dialog':'Cookie preferences','announcements_drawer':'Updates and announcements','account_popover':'Account menu','filters_drawer':'Filters','genre_dialog':'Explore genres','search_popover':'Search Roblox','join_dialog':'Join this experience or community','favorite_dialog':'Save to favorites','report_dialog':'Report content','cart_drawer':'Your selection','purchase_dialog':'Confirm simulated purchase','outfit_dialog':'Save outfit','reset_dialog':'Reset avatar?','body_dialog':'Body customization','message_dialog':'Send a message','connection_dialog':'Add connection','invite_dialog':'Invite connections','remove_dialog':'Remove connection?','profile_popover':'Player details','create_dialog':'Create something new','announcement_dialog':'Community announcement','item_dialog':'Item details','delete_dialog':'Confirm deletion','compose_dialog':'New message','attachment_dialog':'Attach a file','preferences_dialog':'Notification preferences','notification_popover':'Notification options','clear_dialog':'Clear notifications?','redeem_dialog':'Redeem a code','date_dialog':'Date range','export_dialog':'Export transactions','details_dialog':'Transaction details','password_dialog':'Change password','publish_dialog':'Publish experience','collaborate_dialog':'Invite collaborators','reminder_dialog':'Set an event reminder','share_dialog':'Share this event','settings_dialog':'Experience settings','leave_dialog':'Leave experience?'}.get(state,'Details')
 return d
def reference_theme(mode='dark'):
 dark=mode=='dark';text='#F2F3F5' if dark else '#23262D';surface='#24272D' if dark else '#FFFFFF'
 return dict(mode=mode,semantic={'background':'#17191E' if dark else '#F2F3F5','on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#34383F' if dark else '#E1E4E9','on_surface_variant':text,'primary':'#90B5FF' if dark else '#2459C4','on_primary':'#14203C' if dark else '#FFFFFF','border':'#737983' if dark else '#B7BDC6','icon':text,'error':'#FFB0AF' if dark else '#AF3030'})
