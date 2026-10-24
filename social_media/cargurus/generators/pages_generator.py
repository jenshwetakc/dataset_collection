from __future__ import annotations
import base64,copy,random,html
from functools import lru_cache
from pathlib import Path
PAGE_STATES={
 'home':['used','new','body_style','location_dialog'],
 'results':['listings','map','empty','filter_dialog'],
 'details':['overview','photos','history','contact_dialog'],
 'compare':['two_cars','three_cars','empty','remove_dialog'],
 'saved_cars':['populated','price_drops','empty','remove_dialog'],
 'saved_searches':['populated','editing','empty','alert_dialog'],
 'sell_car':['vehicle_details','condition','offer','vin_help_dialog'],
 'financing':['calculator','prequalify','form_error','consent_dialog'],
 'dealer':['overview','inventory','reviews','contact_dialog'],
 'research':['reviews','article','buying_guides','newsletter_dialog'],
}
MODALS={'location_dialog','filter_dialog','contact_dialog','remove_dialog','alert_dialog','vin_help_dialog','consent_dialog','newsletter_dialog'}
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode('ascii')
@lru_cache(maxsize=64)
def vehicle_art(index=0):
 colors=['#69829B','#B51F35','#E2E6EB','#1F374D','#BBA279','#33665C'];c=colors[index%6]
 wheels = "".join(
     (
         f'<circle cx="{x}" cy="310" r="45" fill="#202932"/>'
         f'<circle cx="{x}" cy="310" r="27" fill="#AAB6C1"/>'
         f'<circle cx="{x}" cy="310" r="10" fill="#445564"/>'
     )
     for x in (219, 544)
 )

 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#C6D5E3"/><stop offset="1" stop-color="#F5F7F9"/></linearGradient><linearGradient id="paint" x2="0" y2="1"><stop stop-color="{c}"/><stop offset="1" stop-color="#233440"/></linearGradient></defs><rect width="720" height="420" fill="url(#sky)"/><path d="M0 320H720V420H0Z" fill="#D1D5DA"/><ellipse cx="370" cy="340" rx="260" ry="24" fill="#81909D" opacity=".3"/><path d="M95 290 L135 238 L235 221 L295 155 Q310 138 345 140 L467 150 Q495 152 515 182 L560 236 L630 257 L646 295 L630 320 H99Z" fill="url(#paint)"/><path d="M259 221 L310 164 H361 V221Z M374 164 L456 171 Q478 173 488 191 L511 225 H374Z" fill="#314F65" stroke="#B7CCD9" stroke-width="3"/><path d="M103 278L171 264 M563 261L626 277" stroke="#EAF6FF" stroke-width="12"/><path d="M170 242H520 M385 227V300" stroke="#ABC0CC" opacity=".6" stroke-width="2"/><rect x="401" y="241" width="23" height="5" rx="2" fill="#C7D5DE"/>{wheels}<text x="30" y="390" font-family="Arial" font-size="14" fill="#65717E">Illustrative vehicle artwork</text></svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode('ascii')
def monthly_payment(principal,apr,months):
 if months<=0 or principal<0 or apr<0:raise ValueError('Invalid financing example')
 r=apr/1200
 return principal/months if r==0 else principal*r/(1-(1+r)**(-months))
def generate_data(sample_index=0,page='home',media_dir:Path|None=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(f'cargurus:{sample_index}');pool=[];encoded={}
 if media_dir and (Path(media_dir)/'vehicles').is_dir():
  from social_media.common.media_generator import get_image_files,image_to_data_uri
  pool=list(get_image_files(str(Path(media_dir)/'vehicles')))
 def image(i):
  if not pool:return vehicle_art(i)
  path=rng.choice(pool)
  if path not in encoded:encoded[path]=image_to_data_uri(path)
  return encoded[path]
 makes=[('Toyota','RAV4','XLE AWD'),('Honda','CR-V','EX AWD'),('Mazda','CX-5','Touring AWD'),('Ford','Escape','SE AWD'),('Hyundai','Tucson','SEL AWD'),('Kia','Sportage','EX AWD'),('Subaru','Forester','Premium AWD'),('Nissan','Rogue','SV AWD'),('Toyota','Camry','SE'),('Honda','Accord','Sport'),('BMW','X3','xDrive30i'),('Volkswagen','Tiguan','SE AWD')]
 cars=[dict(id=i,make=make,model=model,trim=trim,title=f'{2021+i%4} {make} {model} {trim}',year=2021+i%4,price=21950+i*1050,miles=rng.randint(12000,68000),deal=['Great Deal','Good Deal','Fair Deal'][i%3],below=1000+i*150,city=['Boston, MA','Cambridge, MA','Quincy, MA'][i%3],distance=5+i*4,dealer='Northstar Auto Group',rating='4.7',image=image(i),body='Sedan' if i in [8,9] else 'SUV',fuel='Gasoline',transmission='Automatic',drive='AWD' if 'AWD' in trim or i==10 else 'FWD',color=['Blue','Red','White','Gray'][i%4]) for i,(make,model,trim) in enumerate(makes)]
 selected=cars[0]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,dialog_title='',cars=cars,selected=selected,compare_cars=cars[:2],zip='02116',results_count=1284,down_payment=5000,apr=7.5,months=60,monthly=f'{monthly_payment(selected["price"]-5000,7.5,60):.0f}',reviews=[dict(name=n,initials=''.join(s[0] for s in n.split()),date=f'October {9-i}, 2026',text='The team answered my questions clearly and made it easy to arrange a visit.') for i,n in enumerate(['Alex Morgan','Jamie Park','Sam Rivera'])],articles=[dict(title=t,category=c,image=cars[i]['image'],summary='Practical information to help you understand features, costs, and the shopping process.') for i,(t,c) in enumerate([('Choosing the right compact SUV','Buying guide'),('What to check on a used-car test drive','Shopping advice'),('Understanding hybrid and electric options','Research'),('How to compare trim levels','Buying guide'),('Preparing your car for sale','Selling advice'),('Understanding vehicle history reports','Research')])])
def apply_state(base,state):
 d=copy.deepcopy(base)
 if state not in PAGE_STATES[d['page']]:raise ValueError(f'Invalid state {state}')
 d.update(state=state,popup_visible=state in MODALS)
 if state=='three_cars':d['compare_cars']=d['cars'][:3]
 if state=='new':
  for car in d['cars']:car.update(year=2026,title=f'2026 {car["make"]} {car["model"]}',miles=0,deal=None)
 if state=='empty':d['cars']=[];d['results_count']=0
 d['dialog_title']={'location_dialog':'Set your location','filter_dialog':'Refine your search','contact_dialog':'Contact Northstar Auto Group','remove_dialog':'Remove this car?' if d['page']=='saved_cars' else 'Remove from comparison?','alert_dialog':'Manage search alerts','vin_help_dialog':'Where can I find my VIN?','consent_dialog':'Review your information','newsletter_dialog':'Get car-shopping insights'}.get(state,'')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';bg='#18212B' if dark else '#FFFFFF';surface='#22303E' if dark else '#F5F7FA';fg='#F0F4F8' if dark else '#1D2B3A';border='#667788' if dark else '#BCC8D4'
 return {'mode':mode,'semantic':{'background':bg,'surface':surface,'on_background':fg,'on_surface':fg,'primary':'#1B70CF' if dark else '#075BC7','on_primary':'#FFFFFF','border':border,'border_subtle':'#435467' if dark else '#DCE3E9','icon':fg,'surface_variant':'#2B3C4F' if dark else '#EAF1F8','on_surface_variant':'#B8C7D7' if dark else '#5D6D7E'}}
