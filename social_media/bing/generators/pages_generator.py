"""Python 3.10+ compatible synthetic Bing scenarios; all media is local."""
from pathlib import Path
from functools import lru_cache
import base64,copy,random
PAGE_STATES={
'home':['discover','suggestions','rewards','location_dialog'],
'web':['standard','answer_expanded','no_results','feedback_dialog'],
'images':['grid','filtered','empty','image_dialog'],
'videos':['grid','shorts','filtered','video_dialog'],
'news':['top_stories','technology','local','newsletter_dialog'],
'shopping':['products','deals','compare','product_dialog'],
'maps':['places','directions','place_details','share_dialog'],
'weather':['forecast','hourly','air_quality','location_dialog'],
'saved':['collections','collection_detail','empty','collection_dialog'],
'settings':['general','privacy','history','clear_history_dialog']}
MODALS={s for states in PAGE_STATES.values() for s in states if s.endswith('_dialog')}
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=48)
def artwork(i):
 colors=['#427B99','#4E886B','#B66A46','#7B6297','#387B89','#AA8F46'];c=colors[i%len(colors)]
 if i%3==0:
  shapes='<path d="M0 230L140 70 260 230 350 115 520 280 640 170 720 250V420H0Z" fill="#294C60"/><path d="M0 295Q230 205 450 290T720 285V420H0Z" fill="#86B7BF"/><path d="M0 335Q190 265 400 335T720 345V420H0Z" fill="#DFE8DD"/>'
 elif i%3==1:
  shapes='<rect x="220" y="100" width="275" height="175" rx="12" fill="#263B4D"/><rect x="233" y="113" width="249" height="146" rx="6" fill="#A6CCDE"/><path d="M220 275L175 315H540L495 275Z" fill="#D1DFE7"/><path d="M265 315H450" stroke="#263B4D" stroke-width="5"/>'
 else:
  shapes='<rect x="65" y="160" width="590" height="175" rx="8" fill="#E8E3D7"/><path d="M50 160L160 85 260 160 370 65 485 160 570 100 670 160" fill="#334E61"/><g fill="#4F7B95"><rect x="100" y="195" width="65" height="80"/><rect x="205" y="195" width="65" height="80"/><rect x="340" y="185" width="85" height="150"/><rect x="480" y="195" width="65" height="80"/></g>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420"><rect width="720" height="420" fill="'+c+'"/><circle cx="570" cy="75" r="45" fill="#F1D886"/>'+shapes+'<text x="18" y="400" fill="#FFFFFF" font-family="Arial" font-size="13">Illustrative media</text></svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
@lru_cache(maxsize=24)
def product_artwork(i):
 colors=['#23394D','#3F617C','#787E85','#84654E'];c=colors[i%4]
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420"><rect width="720" height="420" fill="#E9EFF4"/><ellipse cx="360" cy="345" rx="160" ry="20" fill="#CDD7DF"/><path d="M220 245V185Q220 70 360 70T500 185V245" fill="none" stroke="'+c+'" stroke-width="36"/><path d="M238 185Q238 90 360 90T482 185" fill="none" stroke="#A9B8C5" stroke-width="8"/><rect x="195" y="200" width="78" height="125" rx="32" fill="'+c+'"/><rect x="447" y="200" width="78" height="125" rx="32" fill="'+c+'"/><rect x="255" y="211" width="25" height="104" rx="12" fill="#1E2933"/><rect x="440" y="211" width="25" height="104" rx="12" fill="#1E2933"/><text x="18" y="400" fill="#5E6C79" font-family="Arial" font-size="13">Illustrative product artwork</text></svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);pool=[]
 if media_dir and Path(media_dir).is_dir():
  from social_media.common.media_generator import get_image_files,image_to_data_uri
  pool=list(get_image_files(str(media_dir)))
 def image(i):return image_to_data_uri(pool[i%len(pool)]) if pool else artwork(i)
 titles=['A weekend guide to the Pacific Northwest','Designing a better home workspace','City gardens and community spaces','Small adventures close to home','Choosing a lightweight travel laptop','A practical guide to sustainable living','Coastal trails worth exploring','What to look for in wireless headphones','Creative ideas for a quiet weekend','A new perspective on urban travel','Planning an autumn photography trip','Making the most of your local library']
 items=[dict(id=i,title=t,image=image(i),source=['Northwest Journal','Design Weekly','City Observer','Travel Notes'][i%4],domain=['northwest.example','design.example','city.example','travel.example'][i%4],description='Explore useful tips, local highlights, expert perspectives, and practical ideas for your next project.',time=str(1+i%5)+' hours ago',price=49+i*17,rating='4.6',duration=f'{3+i}:24',views=f'{12+i*7}K views',category=['Travel','Technology','Local','Lifestyle'][i%4]) for i,t in enumerate(titles)]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,query='Pacific Northwest travel' if page not in ['shopping','maps','weather'] else {'shopping':'wireless headphones','maps':'coffee near Seattle','weather':'Seattle weather'}[page],items=items,products=[dict(items[i],title=t,image=items[i]['image'] if pool else product_artwork(i)) for i,t in enumerate(['Wireless over-ear headphones','Compact noise-cancelling headphones','Studio headphones','Portable wireless earbuds','Everyday Bluetooth headphones','Premium travel headphones','Open-ear sport headphones','Foldable audio headset','Gaming audio headset','Lightweight wireless earbuds','Travel audio kit','Wireless charging case'])],places=[dict(name=n,rating='4.7',reviews=128+i*43,address=f'{120+i*23} Pine Street, Seattle',distance=f'{0.3+i*0.4:.1f} mi',image=image(i+2),open='Open · Closes 8 PM') for i,n in enumerate(['Pine Street Coffee','Harbor Roasters','Evergreen Café','Market Espresso','Lakeview Coffee','Juniper Bakery'])],forecast=[dict(day=d,high=18+i%3,low=10+i%3,glyph=['partly_cloudy_day','rainy','cloud','sunny'][i%4]) for i,d in enumerate(['Today','Wed','Thu','Fri','Sat','Sun','Mon','Tue'])],history=['Pacific Northwest travel','wireless headphones','Seattle weather','coffee near Seattle','autumn hiking routes','home office ideas'],suggestions=['pacific northwest travel itinerary','pacific northwest national parks','pacific northwest road trip','pacific northwest best time to visit','pacific northwest train journeys'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state in MODALS)
 if d['page']=='home' and state!='suggestions':d['query']=''
 if state in ['empty','no_results']:d['items']=[]
 d['dialog_title']={'location_dialog':'Choose your location','feedback_dialog':'Send feedback','image_dialog':'Image details','video_dialog':'Video details','newsletter_dialog':'Get news updates','product_dialog':'Product details','share_dialog':'Share this place','collection_dialog':'Create a collection','clear_history_dialog':'Clear search history'}.get(state,'')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';bg='#181A1D' if dark else '#FFFFFF';surface='#22252A' if dark else '#F5F7FA';text='#E9EDF2' if dark else '#202124';muted='#B6C0CC' if dark else '#58636F';primary='#8ABEFF' if dark else '#0069BE'
 return dict(mode=mode,semantic={'background':bg,'on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#30363D' if dark else '#EAF0F6','on_surface_variant':muted,'primary':primary,'on_primary':'#111820' if dark else '#FFFFFF','border':'#657181' if dark else '#8996A4','border_subtle':'#414A55' if dark else '#DCE2E8','icon':text,'error':'#FFB0AA' if dark else '#B3261E'})
