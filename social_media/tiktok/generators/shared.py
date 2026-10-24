from __future__ import annotations
import copy,random
from pathlib import Path
from social_media.common.media_generator import ASSETS_ROOT,get_image_files,image_to_data_uri
STATES={'for_you': ['playing', 'paused', 'following', 'friends', 'comments', 'share'], 'live': ['watching', 'battle', 'ranking', 'gift_picker', 'viewer_list', 'report'], 'shop': ['recommended', 'category', 'product_detail', 'cart', 'checkout', 'order_success'], 'search': ['top', 'videos', 'users', 'sounds', 'hashtags', 'filters'], 'sound': ['overview', 'popular', 'recent', 'saved', 'use_sound', 'sound_options'], 'creator_studio': ['overview', 'content', 'audience', 'earnings', 'date_range', 'export'], 'video_editor': ['trim', 'sounds', 'effects', 'text', 'caption', 'publish_confirmation'], 'inbox': ['activity', 'messages', 'requests', 'conversation', 'new_message', 'notification_options'], 'profile': ['videos', 'reposts', 'liked', 'private', 'edit_profile', 'followers'], 'privacy_safety': ['privacy', 'comments', 'messages', 'blocked_accounts', 'report_problem', 'delete_account']}
POPUPS={'comments','share','gift_picker','viewer_list','report','product_detail','checkout','order_success','filters','use_sound','sound_options','date_range','export','publish_confirmation','new_message','notification_options','edit_profile','followers','report_problem','delete_account'}
NAV=[('for_you','home','For You'),('live','live_tv','LIVE'),('shop','shopping_bag','Shop'),('search','search','Search'),('sound','music_note','Sounds'),('creator_studio','analytics','TikTok Studio'),('video_editor','add_box','Upload'),('inbox','chat_bubble','Inbox'),('profile','person','Profile'),('privacy_safety','shield','Privacy & safety')]
NAMES=['Alex Chen','Mina Park','Sam Rivera','Jordan Lee','Aria Kim','Noah Patel','Lily Nguyen','Leo Martin','Sofia Garcia','Kai Wilson','Emma Brown','Ethan Davis']
CAPTIONS=['A day in my life ✨ #dailyvlog','Wait for the ending! #fyp','Trying this for the first time #foodtok','A little weekend adventure #travel','Behind the scenes of my studio #creative','Three tips I wish I knew earlier #learnontiktok','This trend was too good to miss #dance','Making something from scratch #diy']
PRODUCTS=['Portable LED light','Everyday canvas tote','Wireless earbuds','Ceramic coffee cup','Skincare starter kit','Desk organizer','Travel water bottle','Compact tripod','Cozy cotton hoodie','Phone stand','Mini blender','Running cap']
def generate_data(page,sample_index=0,assets_dir=None):
 if page not in STATES:raise ValueError(page)
 root=Path(assets_dir) if assets_dir else ASSETS_ROOT/'tiktok'
 avatars=get_image_files(str(root/'avatars'));photos=get_image_files(str(root/'posters')) or get_image_files(str(root)) or get_image_files(str(ASSETS_ROOT))
 if not photos:raise FileNotFoundError(f'Add jpg/png/webp images to {root} or pass --assets-dir')
 avatars=avatars or photos;cache={}
 def image(pool):
  p=random.choice(pool)
  if p not in cache:cache[p]=image_to_data_uri(p)
  return cache[p]
 users=[{'id':f'u{i}','name':NAMES[i%len(NAMES)],'username':NAMES[i%len(NAMES)].lower().replace(' ','_')+str(i),'avatar':image(avatars),'selected':i<2,'followers':random.randint(1000,900000)} for i in range(24)]
 videos=[{'id':f'v{i}','author':users[i%24],'image':image(photos),'caption':random.choice(CAPTIONS),'likes':random.randint(100,99000),'comments':random.randint(10,9500),'shares':random.randint(10,5000),'views':random.randint(1000,900000),'duration':random.choice(['0:18','0:32','1:04','0:47']),'liked':i%3==0,'saved':i%4==0} for i in range(30)]
 products=[{'id':f'product{i}','name':n,'image':image(photos),'price':round(random.uniform(8,80),2),'rating':round(random.uniform(4.2,5),1),'sold':random.randint(300,20000),'selected':i<2} for i,n in enumerate(PRODUCTS)]
 return {'page':page,'state':STATES[page][0],'popup_visible':False,'navigation':NAV,'viewer':users[0],'users':users,'videos':videos,'active_video':videos[0],'products':products,'active_product':products[0],'query':'weekend ideas','comments':[{'author':users[i+1],'text':random.choice(['Love this!','How did you make this?','Part two please!','The ending 😂','Saved for later','This is so helpful']),'liked':i%3==0} for i in range(12)],'sounds':[{'title':n,'artist':NAMES[i],'uses':random.randint(1000,200000),'duration':'0:30','image':image(photos)} for i,n in enumerate(['Original sound','Weekend mood','Golden hour','City lights','Little moments','Summer again','Midnight drive','Good energy'])],'gifts':[{'name':n,'icon':ic,'coins':c} for n,ic,c in [('Rose','local_florist',1),('Heart','favorite',5),('Coffee','coffee',20),('Music','music_note',99),('Crown','workspace_premium',299),('Fireworks','celebration',999),('Star','star',100),('Rocket','rocket_launch',1000)]],'sample_index':sample_index,'chart':[26,42,35,63,51,84,72,95,66,89,100,82],'settings':[('Private account','lock'),('Activity status','circle'),('Allow comments','chat_bubble'),('Allow downloads','download'),('Allow Duet','view_column'),('Allow Stitch','content_cut'),('Suggest your account','person_add'),('Personalized ads','ads_click')],'cart_total':round(products[0]['price']+products[1]['price'],2)}
def apply_state(base,state):
 if state not in STATES[base['page']]:raise ValueError(state)
 d=copy.deepcopy(base);d['state']=state;d['popup_visible']=state in POPUPS and not (d['page']=='privacy_safety' and state=='comments')
 if d['page']=='for_you' and state in {'following','friends'}:d['videos']=d['videos'][::2];d['active_video']=d['videos'][0]
 return d
