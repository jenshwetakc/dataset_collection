"""Synthetic Apple-style content, Python 3.10+; prices are illustrative."""
from pathlib import Path
import base64, copy, random
from functools import lru_cache
PAGE_STATES={
'home':['featured','seasonal','cookie_dialog','region_dialog','promotion_dialog'],
'store':['catalog','education','search_dialog','bag_drawer','cookie_dialog'],
'mac':['overview','configuration','compare_dialog','tradein_dialog','financing_dialog'],
'iphone':['overview','configuration','color_dialog','tradein_dialog','delivery_dialog'],
'ipad':['overview','configuration','accessory_dialog','education_dialog','cookie_dialog'],
'watch':['overview','configuration','size_dialog','band_dialog','delivery_dialog'],
'airpods':['overview','configuration','engraving_dialog','compare_dialog','promotion_dialog'],
'compare':['models','differences','model_dialog','share_dialog','cookie_dialog'],
'bag':['items','empty','checkout_dialog','remove_dialog','delivery_dialog'],
'support':['topics','results','contact_dialog','appointment_dialog','error_dialog']}
@lru_cache(maxsize=1)
def font_uri():
 return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=64)
def art(kind,i=0):
 c=['#B6C9DF','#D6BCB0','#B9C7B0','#ACA9C8'][i%4]
 if kind=='mac': shapes='<rect x="155" y="60" width="490" height="290" rx="20" fill="#35373B"/><rect x="170" y="76" width="460" height="255" rx="8" fill="'+c+'"/><path d="M155 350L95 395H705L645 350Z" fill="#BFC2C8"/>'
 elif kind=='airpods': shapes='<path d="M275 165Q245 85 320 85Q375 85 360 145L340 300" stroke="#E5E5E9" stroke-width="45" fill="none"/><path d="M525 165Q555 85 480 85Q425 85 440 145L460 300" stroke="#E5E5E9" stroke-width="45" fill="none"/><rect x="300" y="300" width="200" height="100" rx="42" fill="#FFFFFF" stroke="#B8B8C0"/>'
 elif kind=='watch': shapes='<rect x="342" y="20" width="116" height="400" rx="38" fill="'+c+'"/><rect x="302" y="115" width="196" height="210" rx="55" fill="#9EA0A7"/><rect x="312" y="125" width="176" height="190" rx="48" fill="#202127"/><circle cx="400" cy="220" r="58" fill="none" stroke="#FF6B63" stroke-width="12"/><path d="M400 220V178M400 220L433 242" stroke="#FFFFFF" stroke-width="8"/>'
 else: shapes='<rect x="275" y="30" width="250" height="385" rx="35" fill="#33353B"/><rect x="285" y="40" width="230" height="365" rx="28" fill="'+c+'"/><ellipse cx="400" cy="210" rx="100" ry="155" fill="#6E82A3"/><rect x="364" y="48" width="72" height="20" rx="10" fill="#25262C"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450"><rect width="800" height="450" fill="#F5F5F7"/>'+shapes+'</svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 products=[]
 names=[('mac','MacBook Air'),('mac','MacBook Pro'),('iphone','iPhone Pro'),('iphone','iPhone'),('ipad','iPad Pro'),('ipad','iPad Air'),('watch','Apple Watch'),('watch','Apple Watch Ultra'),('airpods','AirPods Pro'),('airpods','AirPods'),('mac','Studio Display'),('iphone','Accessories')]
 for i,(kind,name) in enumerate(names):
  image=art(kind,i)
  if media_dir:
   files=sorted(p for p in (Path(media_dir)/kind).glob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
   if files:
    p=files[(sample_index+i)%len(files)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];image='data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  products.append(dict(id=i,kind=kind,name=name,image=image,price=199+i*100,caption=['Power for everything you do.','Designed around your day.','More possibilities. Less limits.'][i%3]))
 selected=next((p for p in products if p['kind']==page),products[0])
 return dict(page=page,state=PAGE_STATES[page][0],font_uri=font_uri(),popup_visible=False,products=products,selected=selected,tab_labels=['Apple — '+page.title(),'Compare models','Your Bag'],quantity=2,query='battery',sample_index=sample_index)
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith('_dialog') or state.endswith('_drawer'))
 d['dialog_title']={'cookie_dialog':'Privacy preferences','region_dialog':'Choose your country or region','promotion_dialog':'Discover a limited-time offer','search_dialog':'Search apple.com','bag_drawer':'Your Bag','tradein_dialog':'Estimate your trade-in','financing_dialog':'Payment options','delivery_dialog':'Delivery and pickup','color_dialog':'Choose a finish','accessory_dialog':'Complete your setup','education_dialog':'Education eligibility','size_dialog':'Find your case size','band_dialog':'Choose your band','engraving_dialog':'Personalize your AirPods','compare_dialog':'Compare models','model_dialog':'Choose a model','share_dialog':'Share this comparison','checkout_dialog':'Checkout','remove_dialog':'Remove this item?','contact_dialog':'Contact Apple Support','appointment_dialog':'Book an appointment','error_dialog':'Unable to load appointments'}.get(state,'Details')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';text='#F5F5F7' if dark else '#1D1D1F';bg='#171719' if dark else '#FFFFFF';surface='#252527' if dark else '#F5F5F7'
 return dict(mode=mode,semantic={'background':bg,'on_background':text,'surface':surface,'on_surface':text,'surface_variant':surface,'on_surface_variant':text,'primary':'#8DBFFF' if dark else '#0066CC','on_primary':'#101010' if dark else '#FFFFFF','border':'#83838A','icon':text,'error':'#FFB0AA' if dark else '#B3261E'})
