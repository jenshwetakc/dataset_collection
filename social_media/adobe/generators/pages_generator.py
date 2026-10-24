"""Fictional Adobe-style screenshot data and scenarios; Python 3.10+."""
import base64,copy,random
from functools import lru_cache
from pathlib import Path
PAGE_STATES={
'home':['featured','photography','business','cookie_dialog','products_popover','account_popover'],
'products':['all_apps','design','video','trial_dialog','compare_dialog','cookie_dialog'],
'creative_cloud':['overview','installed','updates','install_dialog','update_dialog','notifications_drawer'],
'files':['recent','shared','deleted','upload_dialog','share_dialog','delete_dialog'],
'libraries':['assets','colors','fonts','new_library_dialog','add_asset_dialog','share_dialog'],
'stock':['search','photos','videos','filters_drawer','license_dialog','cookie_dialog'],
'asset_detail':['overview','similar','licensing','license_dialog','collection_dialog','report_dialog'],
'express':['templates','projects','brands','new_project_dialog','resize_dialog','export_dialog'],
'express_editor':['design','text','layers','export_dialog','share_dialog','color_dialog'],
'firefly':['explore','generated','history','prompt_dialog','settings_drawer','credits_dialog'],
'acrobat':['recent','shared','starred','upload_dialog','convert_dialog','request_signature_dialog'],
'pdf_editor':['reading','comments','organize','export_dialog','signature_dialog','delete_page_dialog'],
'lightroom':['gallery','albums','favorites','import_dialog','album_dialog','share_dialog'],
'fonts':['browse','activated','families','activation_dialog','filters_drawer','cookie_dialog'],
'behance':['discover','following','moodboards','project_dialog','save_dialog','cookie_dialog'],
'learn':['recommended','photoshop','courses','enrollment_dialog','filters_drawer','cookie_dialog'],
'tutorial':['lesson','transcript','resources','feedback_dialog','download_dialog','subscribe_dialog'],
'pricing':['individuals','teams','students','checkout_dialog','compare_dialog','cookie_dialog'],
'account':['profile','plans','security','edit_profile_dialog','billing_dialog','password_dialog'],
'support':['topics','results','contact','contact_dialog','issue_dialog','cookie_dialog']}

APP_INFO=[('Photoshop','Ps','#13223A','#7FC8FF','Edit images and bring creative ideas to life.','Design'),('Illustrator','Ai','#30210C','#FFBF69','Create vector graphics, illustrations, and brand assets.','Design'),('Premiere Pro','Pr','#20143D','#BCA3FF','Edit video and tell your story with precision.','Video'),('Acrobat','Ac','#401316','#FF9A9F','Work with PDFs, signatures, and document workflows.','Documents'),('Adobe Express','Ex','#28134A','#D9ADFF','Create social graphics, presentations, and more.','Design'),('Lightroom','Lr','#102B3B','#8BD8FF','Organize, edit, and share your photographs.','Photography'),('After Effects','Ae','#21143D','#BEA7FF','Create motion graphics and visual effects.','Video'),('InDesign','Id','#3F1026','#FFA0D4','Design page layouts for print and digital publishing.','Design'),('Firefly','Fi','#3D1847','#E6AFF2','Explore creative possibilities with generative tools.','AI'),('Audition','Au','#12352E','#83DFC7','Record, edit, and mix audio.','Audio'),('Adobe Fonts','Ff','#34152E','#F9ACD7','Find typefaces for your next project.','Design'),('Behance','Be','#113456','#9AC8FF','Discover creative work and share your portfolio.','Community')]
TITLES=['Coastal light studies','Studio brand system','Autumn campaign','Geometric poster series','Editorial layouts','Mountain escape','Product launch kit','Urban perspectives','Motion explorations','Creative workshop','Color and texture','Quiet architecture','Summer collection','Typography in motion','Natural forms','Weekend travel journal','Annual report design','Social content pack','Gallery identity','Illustrated ideas','Ocean stories','Minimal workspace','Festival campaign','Packaging concepts']
NAMES=['Maya Chen','Alex Rivera','Nora Patel','Theo Park','Lina Costa','Sam Morgan','Amir Shah','Emma Brooks','Jules Kim','Ravi Laurent']
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode()
@lru_cache(maxsize=40)
def artwork(i):
 c=['#D8A3A8','#8CB5B4','#B5A8D4','#D7B276','#83A4C6','#A7BE96'][i%6]
 if i%4==0:shapes='<circle cx="490" cy="90" r="52" fill="#FFE1A2"/><path d="M0 270L150 80 330 300 490 130 640 280V400H0Z" fill="#506A80"/><path d="M0 325Q180 215 380 325T640 310V400H0Z" fill="#8FAF9F"/>'
 elif i%4==1:shapes='<rect x="100" y="65" width="240" height="275" rx="8" fill="#253D4F"/><circle cx="220" cy="180" r="74" fill="'+c+'"/><path d="m155 225 65-135 65 135Z" fill="#EACF9C"/><rect x="385" y="120" width="150" height="220" rx="8" fill="#E9E0D1"/><path d="M410 160h100M410 183h100M410 270h65" stroke="#556B77" stroke-width="7"/>'
 elif i%4==2:shapes='<circle cx="240" cy="210" r="155" fill="#305E6A"/><circle cx="360" cy="160" r="120" fill="'+c+'"/><path d="M270 70H530V330H270Z" fill="#E6CF9E" fill-opacity=".8"/><path d="m130 290 300-180M160 320l300-180" stroke="#F4EFE5" stroke-width="12"/>'
 else:shapes='<path d="M80 330V145L220 65l150 90v175Z" fill="#6C8792"/><path d="m80 145 145 85 145-75M225 230v100" fill="none" stroke="#DAE4E2" stroke-width="5"/><path d="M400 330V110h160v220" fill="#E2D7C4"/><path d="M430 145h100M430 180h100M430 215h100" stroke="#819998" stroke-width="10"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 400"><rect width="640" height="400" fill="'+c+'"/>'+shapes+'</svg>'
 return 'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def generate_data(sample_index=0,page='home',media_dir=None):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(sample_index);shift=rng.randrange(24);pool=[]
 if media_dir:pool=sorted(p for p in (Path(media_dir)/'artwork').glob('*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
 def image(i):
  if pool:
   p=pool[(sample_index+i)%len(pool)];ext='jpeg' if p.suffix.lower() in {'.jpg','.jpeg'} else p.suffix[1:];return 'data:image/'+ext+';base64,'+base64.b64encode(p.read_bytes()).decode()
  return artwork(i+sample_index)
 people=[dict(id=i,name=n,initials=''.join(w[0] for w in n.split()),role=['Designer','Photographer','Creative director','Illustrator'][i%4]) for i,n in enumerate(NAMES)]
 apps=[dict(id=i,name=n,short=short,bg=bg,fg=fg,description=desc,category=category,installed=i%3!=0,update=i%4==0) for i,(n,short,bg,fg,desc,category) in enumerate(APP_INFO)]
 assets=[dict(id=i,title=TITLES[(i+shift)%24],image=image(i),author=people[i%10],type=['Photo','Illustration','Video','Template'][i%4],size=['1920 × 1080','3840 × 2160','2400 × 1600'][i%3],likes=124+i*31) for i in range(24)]
 files=[dict(id=i,name=TITLES[(i+shift)%24]+['.psd','.pdf','.ai','.jpg'][i%4],image=image(i),type=['Photoshop','PDF','Illustrator','Image'][i%4],modified='Oct '+str(19-i%15)+', 2026',size=str(2+i*3)+'.4 MB',owner=people[i%10]['name']) for i in range(20)]
 tutorials=[dict(id=i,title=t,image=image(i+5),app=apps[i%8]['name'],duration=str(5+i*3)+' min',level=['Beginner','Intermediate','Advanced'][i%3]) for i,t in enumerate(['Get started with layers','Create a bold social graphic','Improve light and color','Design a flexible brand system','Work with vector shapes','Edit a short video','Prepare a document for sharing','Build a creative moodboard','Explore typography','Organize a photo collection','Create a reusable template','Export for web and print'])]
 return dict(page=page,state=PAGE_STATES[page][0],sample_index=sample_index,font_uri=font_uri(),popup_visible=False,apps=apps,assets=assets,files=files,people=people,tutorials=tutorials,profile=people[0],query='creative workspace',colors=['#E9A89B','#85B6B2','#B7A0D1','#E2C381','#6B90AF','#7F9D78'],marketing=page in ['home','products','pricing','learn','tutorial','support'],editor=page in ['express_editor','pdf_editor'],tab_labels=['Adobe — '+page.replace('_',' ').title(),'Creative Cloud','Studio project'])
def apply_state(data,state):
 if state not in PAGE_STATES[data['page']]:raise ValueError(state)
 d=copy.deepcopy(data);d.update(state=state,popup_visible=state.endswith(('_dialog','_drawer','_popover')))
 d['dialog_title']={'cookie_dialog':'Your privacy choices','products_popover':'Explore Adobe products','account_popover':'Your account','trial_dialog':'Start a simulated trial','compare_dialog':'Compare options','install_dialog':'Install application','update_dialog':'Update application','notifications_drawer':'Notifications','upload_dialog':'Upload files','share_dialog':'Share your work','delete_dialog':'Confirm deletion','new_library_dialog':'Create a library','add_asset_dialog':'Add assets','filters_drawer':'Refine results','license_dialog':'License this asset','collection_dialog':'Save to a collection','report_dialog':'Report content','new_project_dialog':'Create a project','resize_dialog':'Resize design','export_dialog':'Export your work','color_dialog':'Choose a color','prompt_dialog':'Describe your idea','settings_drawer':'Generation settings','credits_dialog':'Your generative credits','convert_dialog':'Convert a document','request_signature_dialog':'Request signatures','signature_dialog':'Add a signature','delete_page_dialog':'Delete this page?','import_dialog':'Import photos','album_dialog':'Create an album','activation_dialog':'Activate font family','project_dialog':'Project details','save_dialog':'Save to a moodboard','enrollment_dialog':'Start this course','feedback_dialog':'Send feedback','download_dialog':'Download resources','subscribe_dialog':'Stay inspired','checkout_dialog':'Review your selection','edit_profile_dialog':'Edit profile','billing_dialog':'Billing details','password_dialog':'Change password','contact_dialog':'Contact support','issue_dialog':'Describe your issue'}.get(state,'Details')
 return d
def reference_theme(mode='light'):
 dark=mode=='dark';text='#F1F1F3' if dark else '#252528';surface='#25262B' if dark else '#FFFFFF'
 return dict(mode=mode,semantic={'background':'#1A1B20' if dark else '#F6F6F8','on_background':text,'surface':surface,'on_surface':text,'surface_variant':'#35373F' if dark else '#ECECF2','on_surface_variant':text,'primary':'#9DAAFF' if dark else '#3E52C5','on_primary':'#151D42' if dark else '#FFFFFF','border':'#737783' if dark else '#C4C6D0','icon':text,'error':'#FFB2AD' if dark else '#B72E30'})
