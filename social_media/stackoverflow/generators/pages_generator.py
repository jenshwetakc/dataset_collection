from __future__ import annotations
import copy,random,base64
from functools import lru_cache
from pathlib import Path
PAGE_STATES={
 'questions':['newest','active','unanswered','filter_dialog'],
 'question':['answered','bounty','closed','flag_dialog'],
 'ask':['writing','validation','preview','discard_dialog'],
 'search':['results','advanced','empty','filter_dialog'],
 'tags':['popular','name_order','watched','tag_dialog'],
 'users':['reputation','new_users','moderators','empty'],
 'profile':['summary','activity','badges','edit_dialog'],
 'saves':['lists','empty','collection','rename_dialog'],
 'collectives':['explore','joined','overview','join_dialog'],
 'settings':['profile','preferences','notifications','delete_dialog'],
}
MODALS={'filter_dialog','flag_dialog','discard_dialog','tag_dialog','edit_dialog','rename_dialog','join_dialog','delete_dialog'}
TITLES={'questions':'Newest Questions','question':'How can I preserve order while removing duplicate objects?','ask':'Ask a public question','search':'Search Results','tags':'Tags','users':'Users','profile':'Alex Morgan','saves':'Saves','collectives':'Collectives','settings':'User settings'}
TOPICS=[('How can I preserve order while removing duplicate objects?',['javascript','arrays']),('Why does my async function return before a callback finishes?',['javascript','async-await']),('How do I merge two DataFrames while keeping unmatched rows?',['python','pandas']),('What is the difference between a flex basis and a width?',['css','flexbox']),('How can I avoid rerendering a list when one item changes?',['reactjs','javascript']),('How should I test a service with an injected database client?',['typescript','unit-testing']),('How do I select the latest record for each group?',['sql','postgresql']),('Why does a dictionary lookup fail after normalizing a string?',['python','dictionary']),('How can I cancel an HTTP request when a component unmounts?',['reactjs','fetch-api']),('What does a detached HEAD mean in a local repository?',['git','version-control']),('How can I keep a toolbar aligned on a narrow screen?',['html','css']),('How can I validate a nested JSON response?',['typescript','json'])]
TAGS=[('javascript','For questions about the JavaScript programming language.'),('python','A general-purpose programming language focused on readability.'),('java','For questions about the Java programming language.'),('c#','A modern language used with the .NET platform.'),('php','A scripting language commonly used for web development.'),('android','Questions about Android development and platform tools.'),('html','The markup language used to structure web content.'),('css','Stylesheets used to control presentation and layout.'),('reactjs','A library for building component-based user interfaces.'),('sql','Questions about querying and managing relational data.'),('typescript','JavaScript with static type checking.'),('git','A distributed version control system.')]
@lru_cache(maxsize=1)
def font_uri():return 'data:font/woff2;base64,'+base64.b64encode((Path(__file__).resolve().parents[1]/'assets/material-symbols-rounded.woff2').read_bytes()).decode('ascii')
def generate_data(sample_index=0,page='questions'):
 if page not in PAGE_STATES:raise ValueError(page)
 rng=random.Random(f'stackoverflow:{page}:{sample_index}')
 questions=[dict(title=t,tags=tags,votes=rng.randint(0,42),answers=rng.randint(0,4),views=rng.randint(38,3500),author=['Jamie Park','Sam Rivera','Maya Patel','Drew Chen'][i%4],time=f'{i+2} min ago',accepted=i%3==0) for i,(t,tags) in enumerate(TOPICS)]
 for q in questions:q['accepted']=q['accepted'] and q['answers']>0
 users=[dict(name=n,initials=''.join(x[0] for x in n.split()),rep=rng.randint(150,68000),location=['Berlin, Germany','Seoul, South Korea','London, United Kingdom','Toronto, Canada'][i%4],tags=['python','javascript']) for i,n in enumerate(['Alex Morgan','Jamie Park','Sam Rivera','Maya Patel','Casey Reed','Jordan Kim','Riley Chen','Drew Lopez','Taylor Singh','Avery Patel','Quinn Lee','Robin Ross'])]
 return dict(page=page,title=TITLES[page],sample_index=sample_index,state=PAGE_STATES[page][0],popup_visible=False,font_uri=font_uri(),questions=questions,users=users,tags=[dict(name=n,desc=desc,count=f'{rng.randint(20,350):,}k') for n,desc in TAGS],query='[javascript]',dialog_title='',draft_title=TOPICS[0][0],body='I have an array of objects with repeated ids. I want to keep the first object for each id and preserve the original order.',code="const items = [\n  { id: 1, name: 'Alpha' },\n  { id: 2, name: 'Beta' },\n  { id: 1, name: 'Alpha' }\n];",answer="const seen = new Set();\nconst unique = items.filter(item => {\n  if (seen.has(item.id)) return false;\n  seen.add(item.id);\n  return true;\n});")
def apply_state(base,state):
 d=copy.deepcopy(base)
 if state not in PAGE_STATES[d['page']]:raise ValueError(f'Invalid state: {state}')
 d.update(state=state,popup_visible=state in MODALS)
 if d['page']=='search':d['questions']=[q for q in d['questions'] if 'javascript' in q['tags']]
 if state=='unanswered':
  for q in d['questions']:q.update(answers=0,accepted=False)
 if state=='active':d['questions'].reverse();d['title']='Active Questions'
 if state=='name_order':d['tags'].sort(key=lambda t:t['name'])
 if state=='new_users':
  for u in d['users']:u['rep']=1
 d['dialog_title']={'filter_dialog':'Filter questions' if d['page']=='questions' else 'Filter search results','flag_dialog':'Flag this question','discard_dialog':'Discard your question draft?','tag_dialog':'Manage watched tag','edit_dialog':'Edit profile','rename_dialog':'Rename your saved list','join_dialog':'Join the Cloud Computing collective','delete_dialog':'Delete your account?'}.get(state,'')
 return d

def reference_theme(mode='light'):
 dark=mode=='dark';bg='#2D2D2D' if dark else '#FFFFFF';sf='#252627' if dark else '#F8F9FA';fg='#E3E6E8' if dark else '#232629';border='#62676C' if dark else '#BABFC4'
 return {'mode':mode,'semantic':{'background':bg,'surface':sf,'on_background':fg,'on_surface':fg,'primary':'#0074CC' if not dark else '#397EC0','on_primary':'#FFFFFF','border':border,'border_subtle':'#494D50' if dark else '#D6D9DC','icon':fg,'surface_variant':'#3B4045' if dark else '#EFF0F1','on_surface_variant':'#B6BDC2' if dark else '#6A737C'}}
