from __future__ import annotations
import base64,copy,random,html
from functools import lru_cache
from pathlib import Path
PAGE_STATES={
 'home':['featured','junior','continue_watching','profile_menu'],
 'search':['discover','results','empty','filter_dialog'],
 'details':['overview','episodes','extras','trailer_dialog'],
 'brand':['featured','movies','series','collection_dialog'],
 'watchlist':['populated','editing','empty','remove_dialog'],
 'downloads':['downloaded','downloading','offline','delete_dialog'],
 'player':['playing','paused','audio_dialog','up_next'],
 'profiles':['chooser','editing','edit_profile','pin_dialog'],
 'account':['overview','subscription','devices','signout_dialog'],
 'settings':['playback','accessibility','parental','rating_dialog'],
}
MODALS={'profile_menu','filter_dialog','trailer_dialog','collection_dialog','remove_dialog','delete_dialog','audio_dialog','up_next','pin_dialog','signout_dialog','rating_dialog'}
TITLES=['The Lantern Voyage','Beyond the Stars','Ocean Guardians','Hidden Kingdom','Moonlight Academy','Wild Horizons','The Last Explorer','City of Dreams','Winter Tales','Cosmic Friends','Island Adventures','The Secret Garden']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode('ascii')
@lru_cache(maxsize=64)
def poster_uri(index,title):
 colors=[('#193F62','#DC9860'),('#221958','#9E9FFF'),('#063647','#67C9CC'),('#203A22','#E9C77A'),('#2D2457','#DF99C6'),('#12382C','#B9D593')];a,b=colors[index%len(colors)]
 words=html.escape(title).split();lines=[' '.join(words[:2]),' '.join(words[2:])]
 text=''.join(f'<text x="320" y="{245+i*48}" text-anchor="middle" fill="white" font-family="Arial" font-size="36" font-weight="700">{line}</text>' for i,line in enumerate(lines) if line)
 credit='<text x="320" y="332" fill="white" opacity=".65" text-anchor="middle" font-family="Arial" font-size="12">ORIGINAL SYNTHETIC ARTWORK</text>' if title else ''
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="640" height="360" fill="url(#g)"/><circle cx="{420-index%4*60}" cy="95" r="52" fill="{b}" opacity=".7"/><path d="M0 220 L150 90 L290 220 L440 120 L640 240 V360 H0Z" fill="{a}" opacity=".7"/><path d="M0 275 Q140 210 300 265 T640 240 V360 H0Z" fill="{a}"/><g fill="white" opacity=".6"><circle cx="60" cy="50" r="3"/><circle cx="160" cy="35" r="2"/><circle cx="535" cy="60" r="3"/></g>{text}{credit}</svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir:Path|None=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(f'disneyplus:{sample_index}');pool=[];banners=[];avatars=[];encoded={}
 if media_dir and Path(media_dir).exists():
  from social_media.common.media_generator import get_image_files,image_to_data_uri
  pool=list(get_image_files(str(Path(media_dir)/'netflix_cover')));banners=list(get_image_files(str(Path(media_dir)/'netflix_cover')));avatars=list(get_image_files(str(Path(media_dir)/'avatars')))
 def image(files,fallback):
  if not files:return fallback
  path=rng.choice(files)
  if path not in encoded:encoded[path]=image_to_data_uri(path)
  return encoded[path]
 catalog=[dict(id=i,title=t,image=image(pool,poster_uri(i,t)),year=2021+i%5,rating='G' if i%4==0 else 'PG' if i%3==0 else '12+',genre=['Adventure','Science Fiction','Documentary','Animation'][i%4],duration='1 Season' if i%3==0 else f'{90+i*3} min',media_type='Series' if i%3==0 else 'Movie',progress=25+i*4,description='An unexpected discovery brings a group of friends together on a journey filled with courage, wonder, and new beginnings.') for i,t in enumerate(TITLES)]
 hero=copy.deepcopy(catalog[0]);hero['image']=image(banners,poster_uri(0,''))
 profiles=[dict(name=n,initial=n[0],color=c,image=image(avatars,'')) for n,c in [('Alex','#2F5688'),('Jamie','#654281'),('Morgan','#34706A'),('Junior','#845021')]]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,dialog_title='',catalog=catalog,brand_catalog=catalog[:8],hero=hero,extras=[dict(catalog[0],title=t,duration=duration,genre='Bonus feature') for t,duration in [('Official Trailer','2 min'),('Behind the Scenes','8 min'),('Meet the Creators','5 min')]],profiles=profiles,active_profile='Alex',query='',results=catalog,supports_downloads=True,episodes=[dict(number=i,title=t,duration=f'{28+i} min',description='The team follows a new clue and faces an unexpected challenge.',image=catalog[i%12]['image']) for i,t in enumerate(['A New Beginning','The Hidden Map','Into the Unknown','Old Friends','Beyond the Horizon','Together Again'],1)],devices=[dict(name=n,location='Seoul, South Korea',last_used=t) for n,t in [('Chrome on Mac','Active now'),('Living Room TV','Yesterday'),('iPhone','2 days ago')]])
def apply_state(base,state):
 d=copy.deepcopy(base)
 if state not in PAGE_STATES[d['page']]:raise ValueError(f'Invalid state: {state}')
 d.update(state=state,popup_visible=state in MODALS)
 if state=='junior':d['active_profile']='Junior';d['catalog']=[x for x in d['catalog'] if x['rating'] in {'G','PG'}]
 if state=='results':d['query']='Ocean';d['results']=[x for x in d['catalog'] if 'Ocean' in x['title']]
 elif state=='empty':d['query']='zzzzzz';d['results']=[]
 d['brand_catalog']=[x for x in d['catalog'] if x['media_type']=='Series'] if state=='series' else [x for x in d['catalog'] if x['media_type']=='Movie'] if state=='movies' else d['catalog'][:8]
 d['dialog_title']={'profile_menu':'Switch profile','filter_dialog':'Search filters','trailer_dialog':'The Lantern Voyage — Trailer','collection_dialog':'About this collection','remove_dialog':'Remove from Watchlist?','delete_dialog':'Delete this download?','audio_dialog':'Audio and subtitles','up_next':'Up next','pin_dialog':'Enter your profile PIN','signout_dialog':'Sign out of all devices?','rating_dialog':'Content rating'}.get(state,'')
 return d
def adapt_to_viewport(data,viewport):
 d=copy.deepcopy(data);category=viewport.get('category','mobile' if viewport['width']<600 else 'desktop')
 d['supports_downloads']=category in {'mobile','mobile_landscape','tablet','foldable'}
 if d['page']=='downloads' and not d['supports_downloads']:d['popup_visible']=False
 return d
def reference_theme(mode='dark'):
 dark=mode=='dark';bg='#0E1421' if dark else '#F5F7FA';surface='#1B2638' if dark else '#FFFFFF';fg='#F9F9F9' if dark else '#182132';border='#65748A' if dark else '#B0BCCB'
 return {'mode':mode,'semantic':{'background':bg,'surface':surface,'on_background':fg,'on_surface':fg,'primary':'#0084A3' if dark else '#006B83','on_primary':'#FFFFFF','border':border,'border_subtle':'#35435A' if dark else '#D7DEE8','icon':fg,'surface_variant':'#263449' if dark else '#E7EDF4','on_surface_variant':'#B9C6D9' if dark else '#556375'}}
