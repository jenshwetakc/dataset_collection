"""Fictional Flickr-style screenshot scenarios, deterministic by seed; Python 3.10+."""
import base64,copy,random
from pathlib import Path
from functools import lru_cache
PAGE_STATES={
'home':['feed','latest','following','cookie_dialog','notifications_drawer','account_popover'],
'explore':['interesting','recent','trending','date_dialog','filters_drawer','cookie_dialog'],
'search':['photos','people','groups','filters_drawer','advanced_dialog','search_popover'],
'photo_detail':['overview','comments','exif','share_dialog','download_dialog','report_dialog'],
'photostream':['justified','grid','list','sort_dialog','edit_profile_dialog','cookie_dialog'],
'albums':['all','favorites','collections','new_album_dialog','edit_album_dialog','delete_dialog'],
'album_detail':['photos','slideshow','map','share_dialog','add_photos_dialog','download_dialog'],
'favorites':['all','people','private','gallery_dialog','remove_dialog','share_dialog'],
'galleries':['discover','yours','featured','new_gallery_dialog','add_photos_dialog','cookie_dialog'],
'gallery_detail':['photos','description','contributors','edit_gallery_dialog','share_dialog','report_dialog'],
'groups':['discover','joined','managed','join_dialog','create_group_dialog','cookie_dialog'],
'group_detail':['pool','discussions','members','add_photos_dialog','invite_dialog','report_dialog'],
'discussion':['thread','reply','unanswered','new_topic_dialog','report_dialog','subscribe_dialog'],
'contacts':['following','followers','suggestions','follow_dialog','remove_dialog','profile_popover'],
'camera_roll':['date_taken','date_uploaded','selected','organize_drawer','privacy_dialog','delete_dialog'],
'upload':['queue','details','finished','file_dialog','album_dialog','privacy_dialog'],
'organizer':['batch','albums','permissions','move_dialog','tags_dialog','delete_dialog'],
'stats':['overview','photos','sources','date_dialog','export_dialog','cookie_dialog'],
'pro':['plans','annual','monthly','checkout_dialog','gift_dialog','cookie_dialog'],
'settings':['account','privacy','notifications','edit_profile_dialog','password_dialog','cookie_dialog']}
TITLES=['Quiet coastal morning','Light between the buildings','Mountain reflections','A study in blue','Golden hour wanderings','Forest after the rain','Windows and stories','Stillness on the water','Patterns in everyday places','Beyond the city lights','Autumn colors','The long way home','Lines and shadows','Weekend on the coast','Desert light','Small details','Clouds over the valley','Old town afternoon','A different perspective','The green trail','Last light at the harbor','Textures of time','Morning in the garden','Open horizons']
NAMES=['Maya Rivers','Alex Chen','Nora Fields','Theo Brooks','Lina Park','Amir Costa','Emma Lane','Ravi Morgan','Sophie Hill','Jules Reed','Sam Woods','Amina Vale']
GROUP_NAMES=['Coastal Light Collective','Urban Perspectives','Everyday Details','Landscape Explorers','Color and Composition','Quiet Moments','Street Stories','Nature in Focus']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=64)
def artwork(i):
 c=['#B6CBD3','#D5B8AB','#BAC7AE','#BFB4D0','#D8C58E','#9BB8B6'][i%6];s=''
 if i%6==0:s='<circle cx="520" cy="85" r="48" fill="#F1DCA2"/><path d="M0 265L160 65 330 280 460 125 640 265V400H0Z" fill="#596F82"/><path d="M0 290L640 245V400H0Z" fill="#94AFB4"/><path d="M80 335H555M180 365h350" stroke="#D7E0D5" stroke-width="5"/>'
 elif i%6==1:s='<path d="M0 285L640 255V400H0Z" fill="#A4B8B8"/><path d="M45 290V110h155v180M245 280V60h125v220M420 270V125h175v145" fill="#5C7782"/><g fill="#DDE6D7"><path d="M70 140h35v40H70ZM130 140h35v40h-35ZM70 210h35v40H70ZM270 95h25v40h-25ZM320 95h25v40h-25ZM270 165h25v40h-25ZM445 160h40v45h-40ZM520 160h40v45h-40Z"/></g><path d="M180 400L300 270h45l80 130" fill="#D8C5A6"/>'
 elif i%6==2:s='<path d="M0 300Q190 160 360 295T640 260V400H0Z" fill="#718F75"/><path d="M0 350Q250 250 640 340V400H0Z" fill="#A4B68B"/><g fill="#355F57"><path d="m40 290 70-210 70 210ZM200 290l60-190 60 190ZM400 260l75-220 75 220Z"/></g><g fill="#6A5948"><path d="M100 275h20v100h-20ZM250 280h20v90h-20ZM465 245h20v110h-20Z"/></g><path d="m285 400 80-110 45 110" fill="#D8C6A0"/>'
 elif i%6==3:s='<circle cx="225" cy="200" r="155" fill="#496D7C"/><circle cx="360" cy="160" r="120" fill="'+c+'"/><rect x="315" y="65" width="225" height="270" fill="#E2D1AF" fill-opacity=".85"/><path d="m100 290 350-185M140 335l350-185" stroke="#E8E5D5" stroke-width="12"/>'
 elif i%6==4:s='<circle cx="500" cy="95" r="60" fill="#EDCE86"/><path d="M0 220Q180 90 380 230T640 190V400H0Z" fill="#BB8D70"/><path d="M0 300Q200 165 420 300T640 250V400H0Z" fill="#D2AD82"/><path d="M0 365Q200 280 420 355T640 330V400H0Z" fill="#E5C69C"/>'
 else:s='<path d="M0 240H640V400H0Z" fill="#6F9DA9"/><path d="M0 325L640 285" stroke="#D5E2D9" stroke-width="6"/><path d="M95 335V180h25v155M105 180l100 65H20Z" fill="#E2D7BA"/><path d="M295 330V145h30v185M310 145l130 100H185Z" fill="#D6B3A0"/><path d="M480 320V200h20v120M490 200l80 60H420Z" fill="#D8D6C7"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400"><rect width="640" height="400" fill="'+c+'"/>'+s+'</svg>';return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);shift=rng.randrange(24);pool=[]
 if media_dir:pool=sorted(p for p in (Path(media_dir)/'photos').glob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
 def image(i):
  if pool:
   p=pool[(sample_index+i)%len(pool)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];return 'data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  return artwork(i+sample_index)
 people=[dict(id=i,name=n,initials=''.join(w[0] for w in n.split()),photos=280+i*137,followers=1200+i*253,bio=['Photographer exploring light, place, and the details of everyday life.','Collecting quiet moments and sharing new perspectives.','Landscape, street, and visual stories from a curious observer.'][i%3]) for i,n in enumerate(NAMES)]
 photos=[dict(id=i,title=TITLES[(i+shift)%24],image=image(i),author=people[i%12],faves=84+i*23,comments=4+i*3,views=1200+i*147,date='Oct '+str(20-i%15)+', 2026',tags=['landscape','light','travel','nature'] if i%2==0 else ['urban','architecture','street','color'],camera=['Mirrorless camera','Compact camera','DSLR camera'][i%3],description='An original illustrative scene for a fictional photo-sharing profile. Add your own photo assets to replace this artwork.') for i in range(24)]
 albums=[dict(id=i,title=t,count=18+i*7,image=image(i+3),description='A curated selection of light, places, and everyday observations.') for i,t in enumerate(['Coastal mornings','City stories','Mountain weekends','Light studies','Quiet moments','Autumn walks','Far from home','Personal favorites'])]
 groups=[dict(id=i,name=n,members=4200+i*1760,photos=58000+i*14600,image=image(i+2),description='A fictional photography community for sharing images, constructive feedback, and creative ideas.') for i,n in enumerate(GROUP_NAMES)]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,photos=photos,people=people,albums=albums,groups=groups,profile=people[0],query='coastal light',tab_labels=['Flickr — '+page.replace('_',' ').title(),'Quiet coastal morning','Your albums'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith(('_dialog','_drawer','_popover')))
 d['dialog_title']={'cookie_dialog':'Your privacy preferences','notifications_drawer':'Notifications','account_popover':'Your account','date_dialog':'Choose a date','filters_drawer':'Filter photos','advanced_dialog':'Advanced search','search_popover':'Search Flickr','share_dialog':'Share this photo or collection','download_dialog':'Download options','report_dialog':'Report content','sort_dialog':'Sort your photostream','edit_profile_dialog':'Edit your profile','new_album_dialog':'Create an album','edit_album_dialog':'Edit album details','delete_dialog':'Confirm deletion','add_photos_dialog':'Add photos','gallery_dialog':'Add to a gallery','remove_dialog':'Remove this item?','new_gallery_dialog':'Create a gallery','edit_gallery_dialog':'Edit gallery details','join_dialog':'Join this group','create_group_dialog':'Create a group','invite_dialog':'Invite photographers','new_topic_dialog':'Start a discussion','subscribe_dialog':'Follow this discussion','follow_dialog':'Follow photographers','profile_popover':'Photographer details','organize_drawer':'Organize selected photos','privacy_dialog':'Photo privacy','file_dialog':'Choose photos','album_dialog':'Add to an album','move_dialog':'Move selected photos','tags_dialog':'Edit tags','export_dialog':'Export statistics','checkout_dialog':'Review your plan','gift_dialog':'Give a Pro membership','password_dialog':'Change password'}.get(state,'Details')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';text='#F0F1F3' if dark else '#24272B';surface='#272A30' if dark else '#FFFFFF'
 return dict(mode=mode,semantic={'background':'#191C21' if dark else '#F3F5F6','on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#363B44' if dark else '#E7ECF0','on_surface_variant':text,'primary':'#86BEF5' if dark else '#006CC1','on_primary':'#112844' if dark else '#FFFFFF','border':'#73808E' if dark else '#BCC6CE','icon':text,'error':'#FFB0AE' if dark else '#B32D31'})
