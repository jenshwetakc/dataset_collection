from __future__ import annotations
import copy
import random
from pathlib import Path

PAGE_STATES={
 'legal':['landing','practice_areas','validation_error','consultation_confirmed','consultation_dialog'],
 'charity':['landing','campaigns','validation_error','donation_confirmed','donation_dialog'],
 'real_estate':['landing','properties','validation_error','tour_confirmed','property_dialog'],
 'fitness':['landing','classes','validation_error','membership_confirmed','membership_dialog'],
 'pool_services':['landing','services','validation_error','quote_confirmed','quote_dialog'],
 'enterprise_ai':['landing','solutions','validation_error','demo_confirmed','demo_dialog'],
 'travel':['landing','tour_results','validation_error','booking_confirmed','booking_dialog'],
 'fintech':['landing','pricing','validation_error','account_created','signup_dialog'],
 'solar':['landing','projects','validation_error','assessment_confirmed','assessment_dialog'],
 'healthcare':['landing','doctors','validation_error','appointment_confirmed','appointment_dialog'],
}
# index corresponds to the reference_map.json supplied with this package.
CONFIG={
 'legal':dict(brand='ENSAF',seed='#9F743F',mode='light',ref=0,eyebrow='YOUR LEGAL SHIELD',title='Experienced Lawyers. Proven Results.',intro='Clear advice, trusted representation, and a dedicated team by your side.',cta='Free consultation',alt='Practice areas',dialog='Book a legal consultation',services=['Corporate law','Family law','Real estate law','Criminal defense','Estate planning','Employment law'],stats=['25+ years of experience','1,850 cases resolved','98% client satisfaction','42 legal specialists'],about='A legacy of legal excellence',feature='Committed to justice. Dedicated to you.',nav=['Home','About us','Practice areas','Cases','Our team','Contact']),
 'charity':dict(brand='Donat',seed='#137762',mode='light',ref=1,eyebrow='GIVE HOPE FOR HUMANITY',title='Change Lives with Your Gift',intro='Together we can provide food, education, and a brighter future for every community.',cta='Donate now',alt='Our campaigns',dialog='Make a donation',services=['Clean water for all','Education for every child','Emergency food relief','Community healthcare','Build a safe home','Support local families'],stats=['120 communities','24,000 people supported','600 volunteers','85 active campaigns'],about='Transforming lives, one donation at a time',feature='Small acts. Extraordinary impact.',nav=['Home','About us','Donations','Projects','Stories','Contact']),
 'real_estate':dict(brand='REALAR',seed='#80700D',mode='light',ref=2,eyebrow='A BETTER PLACE TO CALL HOME',title='Elevate Lifestyle. Luxury Meets Comfort.',intro='Discover exceptional properties in the places you want to live.',cta='Explore properties',alt='Properties',dialog='Schedule a property tour',services=['Seaside modern villa','Skyline penthouse','Garden family residence','Parkview apartment','Hilltop retreat','Lakeside townhome'],stats=['850 elegant apartments','950 luxury houses','18k satisfied guests','2k happy owners'],about='Discover a home that reflects your life',feature='Thoughtful spaces. Exceptional locations.',nav=['Home','About us','Properties','Agents','Journal','Contact']),
 'fitness':dict(brand='FITKIT',seed='#CF2026',mode='dark',ref=3,eyebrow='WELCOME TO FITKIT',title='READY TO TRAIN YOUR BODY',intro='Build strength, improve endurance, and train with a team that supports your goals.',cta='Explore programs',alt='Class schedule',dialog='Choose your membership',services=['Strength training','HIIT conditioning','Personal coaching','Yoga and mobility','Functional fitness','Boxing fundamentals'],stats=['2k active members','35 expert coaches','24 training programs','12 years of experience'],about='Train with purpose. Grow with confidence.',feature='Stronger every day.',nav=['Home','About','Programs','Trainers','Pricing','Contact']),
 'pool_services':dict(brand='Poolax',seed='#007BC4',mode='light',ref=4,eyebrow='REFRESH. RELAX. REJUVENATE.',title='Pool Perfection Starts Here',intro='Professional maintenance and repairs for a sparkling pool in every season.',cta='Get a quote',alt='Our services',dialog='Request a pool service quote',services=['Routine pool cleaning','Water testing','Equipment repair','Pool renovation','Filter maintenance','Seasonal opening'],stats=['25+ years of experience','1,200 happy customers','18 service specialists','98% satisfaction'],about='Simplify pool maintenance with our expert services',feature='Crystal-clear water. Complete peace of mind.',nav=['Home','About us','Services','Projects','Blog','Contact']),
 'enterprise_ai':dict(brand='iSON',seed='#A82E58',mode='light',ref=5,eyebrow='MEET THE NEXT GENERATION OF AI',title='Empathic AI. Where Tech Gets a Heartbeat.',intro='Human-centered intelligence, digital operations, and customer experiences at scale.',cta='Meet our AI',alt='Solutions',dialog='Request an enterprise demo',services=['Customer experience','AI automation','Digital transformation','Cloud operations','Data intelligence','Business process services'],stats=['35 countries','18,000 specialists','120 enterprise partners','24/7 operations'],about='Say hello to a more human digital future',feature='Technology built around people.',nav=['Home','Discover iSON','Services','Industries','Resources','Contact']),
 'travel':dict(brand='Tourm',seed='#087E94',mode='light',ref=6,eyebrow='GET UNFORGETTABLE PLEASURE WITH US',title='Natural Wonder of the World',intro='Thoughtful journeys, unforgettable places, and local experiences you will treasure.',cta='Explore tours',alt='Find your journey',dialog='Book your next adventure',services=['Island escape','Mountain discovery','Cultural city tour','Forest adventure','Desert expedition','Coastal retreat'],stats=['120 destinations','500 curated tours','15k happy travelers','95 local guides'],about='Discover the world your way',feature='Your next chapter starts here.',nav=['Home','About us','Destinations','Tours','Activities','Contact']),
 'fintech':dict(brand='Sassa',seed='#7045D5',mode='light',ref=7,eyebrow='THE BEST SOLUTION IN FINANCE',title='Make the Best Financial Decisions',intro='A clear view of your money, smarter spending, and tools that help you reach your goals.',cta='Get started free',alt='Compare plans',dialog='Create your Sassa account',services=['Smart budgeting','Secure payments','Savings goals','Spending insights','Connected accounts','Investment tracking'],stats=['2m active customers','99.9% uptime','150 countries','4.9 customer rating'],about='All your money, beautifully connected',feature='Built for your financial future.',nav=['Home','About us','Features','Pricing','Resources','Contact']),
 'solar':dict(brand='SOLAK',seed='#428A18',mode='light',ref=8,eyebrow='EMPOWER YOUR FUTURE WITH',title='Solar Power Energy',intro='Reliable solar solutions for homes and businesses, designed for a brighter tomorrow.',cta='Get a free assessment',alt='Our projects',dialog='Schedule a solar assessment',services=['Residential solar','Commercial systems','Battery storage','Panel maintenance','Energy monitoring','EV charging'],stats=['4,200 installations','25 years of expertise','38% average savings','60 energy specialists'],about='Clean energy. Lasting value.',feature='Harness the sun. Power your future.',nav=['Home','About us','Services','Projects','Insights','Contact']),
 'healthcare':dict(brand='Mediax',seed='#07836E',mode='light',ref=9,eyebrow='24/7 EMERGENCY SERVICE',title='Caring for Health. Caring for You.',intro='Compassionate care, experienced specialists, and support for every stage of life.',cta='Appointment now',alt='Find a doctor',dialog='Book an appointment',services=['Primary care','Cardiology','Dental care','Pediatrics','Orthopedics','Diagnostic imaging'],stats=['30 medical specialists','20 years of care','12 departments','24/7 support'],about='Affordable healthcare solutions',feature='Your wellbeing is our priority.',nav=['Home','About us','Services','Doctors','Resources','Contact']),
}
DIALOGS={states[-1] for states in PAGE_STATES.values()}

def generate_data(sample_index:int=0,page:str='legal',assets_dir:Path|None=None)->dict:
 if page not in CONFIG:raise ValueError(f'Unknown page: {page}')
 c=copy.deepcopy(CONFIG[page]);rng=random.Random(f'{page}:{sample_index}')
 c.update(page=page,sample_index=sample_index,state='landing',popup_visible=False,alternate=False,error=False,confirmed=False,media={})
 c['cards']=[{'title':t,'description':['Thoughtful solutions tailored to your needs.','Experienced people and reliable support.','Quality service from the first conversation.'][i%3],'price':f'{rng.randint(150,850):,}','progress':rng.randint(30,85),'tag':['Popular','Featured','New'][i%3]} for i,t in enumerate(c['services'])]
 c['people']=[{'name':n,'role':role,'initials':''.join(s[0] for s in n.split())} for n,role in [('Maya Patel','Senior specialist'),('Alex Morgan','Team lead'),('Jamie Park','Client services'),('Sam Rivera','Program director')]]
 c['faqs']=[('How do I get started?','Contact our team or complete the form below. We will help you choose the right next step.'),('Can I customize the service?','Yes. Our team can tailor the plan to your goals and requirements.'),('What support is included?','Your dedicated team is available to answer questions throughout the process.'),('How do I change my booking?','Contact the team with your booking reference and preferred new date.')]
 if assets_dir:
  from social_media.common.media_generator import get_random_image
  for role in ['hero','about','feature','team']:
   folder=Path(assets_dir)/page/role
   if folder.is_dir():
    uri=get_random_image(folder)
    if uri:c['media'][role]=uri
 return c

def apply_state(base:dict,state:str)->dict:
 d=copy.deepcopy(base)
 if state not in PAGE_STATES[d['page']]:raise ValueError(f'Invalid state for {d["page"]}: {state}')
 d.update(state=state,popup_visible=state in DIALOGS,alternate=state==PAGE_STATES[d['page']][1],error=state=='validation_error',confirmed=state==PAGE_STATES[d['page']][3])
 return d
