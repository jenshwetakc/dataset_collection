from __future__ import annotations
import copy,random,base64,html
from pathlib import Path
from social_media.common.media_generator import ASSETS_ROOT,get_image_files,image_to_data_uri
STATES={'home': ['recommended', 'tv_shows', 'movies', 'continue_watching', 'notifications', 'category_picker'], 'search': ['suggested', 'results', 'no_results', 'genre_results', 'filters', 'voice_search'], 'title_detail': ['overview', 'episodes', 'more_like_this', 'trailers', 'rating', 'share'], 'player': ['playing', 'paused', 'buffering', 'episode_end', 'audio_subtitles', 'playback_error'], 'my_list': ['all', 'movies', 'series', 'empty', 'sort', 'remove_title'], 'new_popular': ['coming_soon', 'everyone_watching', 'top_ten', 'reminder_set', 'reminder_options', 'preview'], 'downloads': ['available', 'downloading', 'expired', 'empty', 'smart_downloads', 'delete_download'], 'profiles': ['choose', 'manage', 'edit', 'add', 'profile_lock', 'delete_profile'], 'account': ['overview', 'membership', 'devices', 'playback_settings', 'change_plan', 'sign_out_devices'], 'kids': ['home', 'characters', 'movies', 'series', 'exit_kids', 'parental_controls']}
POPUPS={'remove_title', 'notifications', 'audio_subtitles', 'change_plan', 'exit_kids', 'preview', 'smart_downloads', 'parental_controls', 'reminder_options', 'category_picker', 'voice_search', 'share', 'filters', 'sort', 'delete_profile', 'sign_out_devices', 'profile_lock', 'rating', 'delete_download'}
NAV=[('home','home','Home'),('search','search','Search'),('title_detail','info','Title'),('player','play_circle','Player'),('my_list','add','My List'),('new_popular','local_fire_department','New & Popular'),('downloads','download','Downloads'),('profiles','person','Profiles'),('account','settings','Account'),('kids','child_care','Kids')]
TITLES=['Beyond the Horizon','The Last Signal','City After Midnight','Wild Earth','The Quiet Harbor','Parallel Lives','Orbit Nine','A Place to Begin','Hidden Trails','Paper Kingdom','Northbound','Second Chances','A Thousand Miles','Night Watch','The Long Weekend','Under the Same Sky','Blue Planet Stories','The Archive','Summer in Motion','Finding Tomorrow','Moonlight Station','Unwritten','The Great Expedition','Echoes of Home']
def svg_uri(svg):return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def art(title,index,wide=False,kids=False):
 color=['#28486c','#573557','#3c594b','#7a4c2e','#3d4169','#683737'][index%6];safe=html.escape(title)
 return svg_uri(f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540"><defs><linearGradient id="g" x2="0" y2="1"><stop stop-color="{color}"/><stop offset="1" stop-color="#09151d"/></linearGradient></defs><rect width="960" height="540" fill="url(#g)"/><circle cx="720" cy="145" r="85" fill="#eedab1" opacity=".65"/><path d="M0 360L160 170L340 350L460 210L660 370L850 250L960 340V540H0Z" fill="#13252e"/><path d="M0 435L240 300L470 455L680 330L960 430V540H0Z" fill="#08141c"/><text x="50" y="405" fill="white" font-family="Arial" font-weight="bold" font-size="48">{safe}</text><text x="52" y="455" fill="#ccdadf" font-family="Arial" font-size="20">SYNTHETIC TITLE ART</text></svg>''')
def avatar(color):
 return svg_uri(f'''<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160"><rect width="160" height="160" rx="12" fill="{color}"/><circle cx="48" cy="62" r="10" fill="white"/><circle cx="112" cy="62" r="10" fill="white"/><path d="M42 100Q80 140 118 100" fill="none" stroke="white" stroke-width="10" stroke-linecap="round"/></svg>''')
def generate_data(page,sample_index=0,assets_dir=None):
 if page not in STATES:raise ValueError(page)
 root=Path(assets_dir) if assets_dir else ASSETS_ROOT
 posters=get_image_files(str(root/'netflix_cover'));backdrops=get_image_files(str(root/'netflix_scene'));avatars=get_image_files(str(root/'avatars'));cache={}
 def media(files,fallback):
  if not files:return fallback
  p=random.choice(files)
  if p not in cache:cache[p]=image_to_data_uri(p)
  return cache[p]
 titles=[]
 for i,name in enumerate(TITLES):
  image=media(posters,art(name,i));backdrop=media(backdrops,image)
  titles.append({'id':f'title{i}','name':name,'image':image,'backdrop':backdrop,'kind':'Series' if i%3 else 'Movie','year':random.randint(2020,2026),'maturity':'TV-14' if i%3 else 'PG-13','seasons':1+i%4,'duration':'1h 48m','genre':['Drama','Adventure','Documentary','Thriller','Comedy','Sci-Fi'][i%6],'match':random.randint(91,99),'progress':random.randint(15,85),'saved':i%3==0,'download_percent':random.randint(20,75),'release':['Friday','October 16','October 23'][i%3],'description':'An unexpected discovery brings a group of strangers together on a journey that could change everything.','cast':'Jordan Vale, Avery Stone, Riley Park','creator':'Morgan Hayes','episodes':[{'number':j+1,'name':n,'duration':45+j%4,'description':'The team follows a new clue as tensions rise and unexpected choices reshape their plans.','image':backdrop} for j,n in enumerate(['A New Beginning','The Discovery','Crossroads','Hidden Truths','A Narrow Escape','The Turning Point','After the Storm','Home Again'])]})
 if page=='kids':
  for i,t in enumerate(titles):
   t['name']=['The Little Explorers','Sunny and Friends','Moon Garden','Pip’s Big Adventure','Learning with Luna','The Puzzle Club','Forest Helpers','Tiny Travelers','Ocean Wonders','The Happy Workshop','Rainbow Road','Max and the Stars'][i%12]
   t['maturity']='TV-Y7';t['genre']='Family';t['description']='Curious friends explore colorful worlds, solve small puzzles, and learn to help each other.'
   if not posters:t['image']=art(t['name'],i,kids=True)
   if not backdrops:t['backdrop']=t['image']
 profiles=[{'name':n,'avatar':media(avatars,avatar(c)),'kids':n=='Kids','locked':n=='Sam'} for n,c in [('Alex','#197fa5'),('Sam','#b74945'),('Taylor','#76873b'),('Kids','#cc973e')]]
 return {'page':page,'state':STATES[page][0],'popup_visible':False,'navigation':NAV,'titles':titles,'title':titles[1],'profiles':profiles,'profile':profiles[0],'query':'horizon','sample_index':sample_index,'devices':[{'name':n,'icon':icon,'location':'Boston, United States','last':'Oct 6, 2026','profile':'Alex'} for n,icon in [('Living room TV','tv'),('Chrome on Windows','computer'),('iPhone','smartphone'),('Android tablet','tablet')]],'genres':['Drama','Comedy','Thrillers','Documentaries','Sci-Fi & Fantasy','Action','Romance','Family'],'storage':{'used':'2.4 GB','free':'18.6 GB'}}
def apply_state(base,state):
 if state not in STATES[base['page']]:raise ValueError(state)
 d=copy.deepcopy(base);d['state']=state;d['popup_visible']=state in POPUPS
 if state in ['tv_shows','series']:d['titles']=[t for t in d['titles'] if t['kind']=='Series']
 if state=='movies':d['titles']=[t for t in d['titles'] if t['kind']=='Movie']
 if state=='genre_results':d['titles']=[t for t in d['titles'] if t['genre']=='Drama']
 if state=='results':d['titles']=[t for t in d['titles'] if d['query'] in t['name'].lower()]
 if state in ['empty','no_results']:d['titles']=[]
 if d['page'] in ['home','kids'] and d['titles']:d['title']=d['titles'][0]
 if state=='add':d['profile']={'name':'','avatar':avatar('#76538e'),'kids':False,'locked':False}
 return d
