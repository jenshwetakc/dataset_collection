"""Deterministic fictional ResearchGate-style screenshot scenarios, Python 3.10+."""
import base64,copy,random
from pathlib import Path
from functools import lru_cache
PAGE_STATES={
'feed':['recommended','following','saved','cookie_dialog','share_dialog','notifications_popover'],
'search':['publications','researchers','no_results','filters_drawer','save_search_dialog','cookie_dialog'],
'publication':['full_text','request_only','references','request_dialog','citation_dialog','report_dialog'],
'profile':['overview','research','stats','edit_profile_dialog','follow_dialog','message_dialog'],
'questions':['recommended','unanswered','following','ask_dialog','topic_dialog','cookie_dialog'],
'question_detail':['discussion','answer_editor','accepted_answer','answer_dialog','report_dialog','share_dialog'],
'network':['suggestions','followers','following','invite_dialog','remove_dialog','researcher_popover'],
'jobs':['recommended','saved','job_detail','job_alert_dialog','apply_dialog','filters_drawer'],
'messages':['inbox','conversation','requests','compose_dialog','attachment_dialog','delete_dialog'],
'settings':['account','privacy','notifications','password_dialog','cookie_dialog','delete_dialog']}
TITLES=['Evaluating visual accessibility in adaptive user interfaces','Reproducible benchmarks for scientific machine learning','Human-centered methods for trustworthy automation','Understanding collaborative research networks','Multimodal representations for document understanding','Measuring uncertainty in real-world prediction systems','A systematic review of software testing practices','Efficient learning with limited annotated data','Open research infrastructure for scientific discovery','User experience across mobile and desktop platforms','Detecting interface defects through visual analysis','Transparent reporting in empirical research']
NAMES=['Maya Chen','Daniel Morgan','Amina Patel','Lucas Rivera','Hana Park','Nora Williams','Elias Schmidt','Sofia Tanaka','Omar Hassan','Emma Laurent','Arjun Mehta','Lina Costa']
TOPICS=['Human–Computer Interaction','Machine Learning','Software Engineering','Computer Vision','Data Science','Research Methods','Open Science','Accessibility']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=40)
def figure(i):
 colors=['#008078','#4E7E9D','#A27548','#74619D'];c=colors[i%4]
 bars=''.join('<rect x="'+str(70+j*65)+'" y="'+str(250-(j*31+i*13)%170)+'" width="36" height="'+str(60+(j*31+i*13)%170)+'" fill="'+c+'"/>' for j in range(6))
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 350"><rect width="500" height="350" fill="#FFFFFF"/><path d="M50 40V310H460" stroke="#606F78" fill="none"/>'+bars+'<text x="55" y="30" font-family="Arial" font-size="18" fill="#253238">Synthetic experiment '+str(i+1)+'</text></svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='feed',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);shift=rng.randrange(len(TITLES))
 people=[dict(id=i,name=n,initials=''.join(w[0] for w in n.split()),institution=['Northbridge University','Westlake Institute of Technology','Center for Open Research','Coastal Science University'][i%4],field=TOPICS[i%len(TOPICS)],publications=24+i*7,citations=152+i*103) for i,n in enumerate(NAMES)]
 papers=[]
 for i in range(12):
  image=figure(i)
  if media_dir:
   files=sorted(p for p in (Path(media_dir)/'figures').glob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
   if files:
    p=files[(sample_index+i)%len(files)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];image='data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  papers.append(dict(id=i,title=TITLES[(i+shift)%len(TITLES)],authors=[people[i%12]['name'],people[(i+1)%12]['name']],date=['October 2026','September 2026','August 2026'][i%3],journal=['Journal of Interactive Systems','Computational Research Review','Open Methods Quarterly'][i%3],kind=['Article','Preprint','Conference Paper'][i%3],reads=230+i*137,citations=3+i*7,recommendations=7+i*3,image=image,abstract='This fictional study investigates practical methods, reproducible evaluation, and empirical evidence across diverse datasets. We describe the experimental protocol, compare alternative approaches, and discuss limitations and implications for future research.'))
 jobs=[dict(id=i,title=t,place=['Northbridge University','Open Research Lab','Westlake Institute'][i%3],location=['Seoul, South Korea','Berlin, Germany','Remote','Toronto, Canada'][i%4],type=['Postdoctoral researcher','PhD position','Research scientist'][i%3],deadline='November '+str(5+i)+', 2026') for i,t in enumerate(['Postdoctoral Fellow in Human–Computer Interaction','PhD Researcher in Responsible AI','Research Scientist — Computer Vision','Assistant Professor in Data Science','Research Software Engineer','Doctoral Fellowship in Accessibility','Postdoc in Scientific Computing','Machine Learning Research Fellow'])]
 questions=[dict(id=i,title=t,author=people[i%12]['name'],answers=3+i*2,reads=125+i*52,topic=TOPICS[i%8]) for i,t in enumerate(['How do you evaluate accessibility across different themes?','Which metrics best capture model uncertainty?','How can we improve reproducibility in empirical studies?','What is a good protocol for comparing visual detectors?','How do you report annotation agreement?','Which sampling strategy works with limited labels?','How do you share research artifacts sustainably?','What methods support mixed-methods evaluation?','How should we evaluate cross-platform consistency?','What are common threats to validity in user studies?'])]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,people=people,papers=papers,jobs=jobs,questions=questions,topics=TOPICS,query='visual accessibility',active_profile=people[0],tab_labels=['ResearchGate — '+page.replace('_',' ').title(),'Publication details','Research network'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith(('_dialog','_drawer','_popover')))
 d['dialog_title']={'cookie_dialog':'Your privacy choices','share_dialog':'Share with your network','notifications_popover':'Notifications','filters_drawer':'Refine your results','save_search_dialog':'Save this search','request_dialog':'Request full-text','citation_dialog':'Cite this publication','report_dialog':'Report content','edit_profile_dialog':'Edit profile','follow_dialog':'Follow this researcher','message_dialog':'Send a message','ask_dialog':'Ask a question','topic_dialog':'Choose research topics','answer_dialog':'Write your answer','invite_dialog':'Invite a colleague','remove_dialog':'Remove this connection?','researcher_popover':'Researcher summary','job_alert_dialog':'Create a job alert','apply_dialog':'Apply for this position','compose_dialog':'New message','attachment_dialog':'Add an attachment','delete_dialog':'Confirm deletion','password_dialog':'Change password'}.get(state,'Details')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';text='#E8ECEE' if dark else '#263238';surface='#252D31' if dark else '#FFFFFF'
 return dict(mode=mode,semantic={'background':'#182024' if dark else '#F3F5F6','on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#303B40' if dark else '#EAF4F2','on_surface_variant':text,'primary':'#72D4C5' if dark else '#007D73','on_primary':'#102320' if dark else '#FFFFFF','border':'#69797F' if dark else '#C3CED2','icon':text,'error':'#FFB3B3' if dark else '#A92D30'})
