from __future__ import annotations
import copy, random
from pathlib import Path
from faker import Faker
from social_media.common.media_generator import ASSETS_ROOT, get_image_files, image_to_data_uri
F = Faker()
STATES = {'home': ['feed', 'following', 'favorites', 'comments', 'share', 'post_options'], 'explore': ['discover', 'search_results', 'accounts', 'tags', 'post_detail', 'search_filters'], 'reels': ['playing', 'paused', 'muted', 'comments', 'share', 'report'], 'stories': ['viewing', 'paused', 'reply', 'viewers', 'share', 'story_options'], 'profile': ['posts', 'tagged', 'private', 'edit_profile', 'followers', 'profile_options'], 'messages': ['inbox', 'conversation', 'requests', 'new_message', 'chat_details', 'delete_chat'], 'notifications': ['all', 'mentions', 'requests', 'following', 'notification_options', 'remove_notification'], 'create': ['upload', 'crop', 'filters', 'caption', 'discard', 'published'], 'saved': ['collections', 'all_posts', 'collection_detail', 'new_collection', 'edit_collection', 'delete_collection'], 'settings': ['account', 'privacy', 'notifications', 'security', 'logout', 'delete_account']}
POPUPS = {'comments','share','post_options','post_detail','search_filters','report','reply','viewers','story_options','edit_profile','followers','profile_options','new_message','chat_details','delete_chat','notification_options','remove_notification','discard','published','new_collection','edit_collection','delete_collection','logout','delete_account'}
NAV = [('home','home','Home'),('explore','explore','Explore'),('reels','movie','Reels'),('stories','amp_stories','Stories'),('profile','person','Profile'),('messages','chat_bubble','Messages'),('notifications','favorite','Notifications'),('create','add_box','Create'),('saved','bookmark','Saved'),('settings','settings','Settings')]
def generate_data(page, sample_index=0, assets_dir=None):
    if page not in STATES: raise ValueError(page)
    root=Path(assets_dir) if assets_dir else ASSETS_ROOT/'instagram'
    files=get_image_files(str(root)) or get_image_files(str(ASSETS_ROOT))
    if not files: raise FileNotFoundError(f'Add jpg/png/webp images to {root} or {ASSETS_ROOT}')
    cache={}
    def image():
        path=random.choice(files)
        if path not in cache: cache[path]=image_to_data_uri(path)
        return cache[path]
    users=[{'id':f'u{i}','username':F.user_name()+str(i),'name':F.name(),'avatar':image(),'selected':i<2,'verified':i%4==0} for i in range(24)]
    posts=[{'id':f'p{i}','author':users[i%24],'image':image(),'caption':F.sentence(nb_words=12),'likes':random.randint(30,20000),'comments':random.randint(5,200),'liked':i%3==0,'saved':i%4==0,'location':F.city(),'age':str(i+1)+'h','kind':'carousel' if i%3==0 else 'photo'} for i in range(30)]
    return {'page':page,'state':STATES[page][0],'popup_visible':False,'navigation':NAV,'viewer':users[0],'users':users,'posts':posts,'active_post':posts[0],'comments':[{'author':users[i+1],'text':F.sentence(),'age':str(i+1)+'m'} for i in range(12)],'collections':[{'name':n,'count':random.randint(12,150),'image':posts[i]['image']} for i,n in enumerate(['Weekend ideas','Travel inspiration','Food favorites','Design details','Places to visit','Creative studio','Outfit ideas','Architecture'])],'messages':[{'author':users[i+1],'text':F.sentence(),'unread':i%3==0,'age':str(i+1)+'m'} for i in range(18)],'sample_index':sample_index,'bio':F.sentence(nb_words=18),'selected_count':2,'query':'travel','settings_rows':[('Private account','lock'),('Activity status','circle'),('Story replies','reply'),('Message requests','chat'),('Two-factor authentication','security'),('Login alerts','notifications')],'upload_image':posts[1]['image']}
def apply_state(base,state):
    page=base['page']
    if state not in STATES[page]: raise ValueError(f'Unknown {page} state: {state}')
    d=copy.deepcopy(base);d['state']=state;d['popup_visible']=state in POPUPS
    if page=='home' and state=='following':d['posts']=d['posts'][::2]
    if page=='home' and state=='favorites':d['posts']=d['posts'][::3]
    return d
