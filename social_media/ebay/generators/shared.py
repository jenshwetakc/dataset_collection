from __future__ import annotations
import copy,random
from pathlib import Path
from social_media.common.media_generator import ASSETS_ROOT,get_image_files,image_to_data_uri
STATES={'home': ['recommended', 'deals', 'recently_viewed', 'categories', 'category_menu', 'notifications'], 'search_results': ['grid', 'list', 'filtered', 'no_results', 'filter_dialog', 'sort_menu'], 'item_detail': ['buy_now', 'variations', 'auction', 'out_of_stock', 'image_gallery', 'contact_seller'], 'auctions_offers': ['bidding', 'outbid', 'winning', 'offer_pending', 'place_bid', 'make_offer'], 'cart': ['filled', 'saved_for_later', 'price_changed', 'empty', 'remove_item', 'shipping_options'], 'checkout': ['review', 'address', 'payment', 'coupon_applied', 'address_dialog', 'order_confirmation'], 'my_ebay': ['summary', 'watchlist', 'saved_searches', 'saved_sellers', 'collection', 'watchlist_actions'], 'orders_returns': ['purchases', 'order_detail', 'tracking', 'return_details', 'start_return', 'leave_feedback'], 'seller_hub': ['overview', 'active_listings', 'sold', 'drafts', 'bulk_edit', 'promote_listing'], 'create_listing': ['photos', 'item_specifics', 'pricing', 'shipping', 'preview', 'publish_confirmation']}
POPUPS={'category_menu','notifications','filter_dialog','sort_menu','image_gallery','contact_seller','place_bid','make_offer','remove_item','shipping_options','address_dialog','order_confirmation','watchlist_actions','start_return','leave_feedback','bulk_edit','promote_listing','publish_confirmation'}
NAV=[('home','home','Home'),('search_results','search','Search'),('item_detail','shopping_bag','Item'),('auctions_offers','gavel','Bids & offers'),('cart','shopping_cart','Cart'),('checkout','credit_card','Checkout'),('my_ebay','person','My eBay'),('orders_returns','inventory_2','Orders'),('seller_hub','storefront','Seller Hub'),('create_listing','add_circle','Sell')]
TITLES=['Mirrorless digital camera with 18–55mm lens','Noise cancelling wireless headphones','Vintage leather shoulder bag','Mechanical keyboard, compact layout','Collectible trading card starter set','Refurbished 13-inch laptop, 256GB SSD','Ceramic dinnerware set, 12 pieces','Classic running sneakers, size 9','Vintage automatic wristwatch','Portable Bluetooth speaker','Handcrafted oak desk organizer','Retro handheld game console','Stainless steel coffee grinder','Travel backpack, 30L','Camera tripod with carrying case','Limited edition art print']
CATEGORIES=[('Electronics','devices'),('Fashion','checkroom'),('Collectibles','style'),('Home & Garden','chair'),('Motors','directions_car'),('Sporting Goods','sports_soccer'),('Jewelry & Watches','watch'),('Toys & Hobbies','toys')]
def generate_data(page,sample_index=0,assets_dir=None):
 if page not in STATES:raise ValueError(page)
 root=Path(assets_dir) if assets_dir else ASSETS_ROOT/'ebay'
 files=get_image_files(str(root)) or get_image_files(str(ASSETS_ROOT))
 if not files:raise FileNotFoundError(f'Add jpg/png/webp images to {root} or pass --assets-dir')
 cache={}
 def image():
  p=random.choice(files)
  if p not in cache:cache[p]=image_to_data_uri(p)
  return cache[p]
 items=[]
 for i in range(32):
  price=round(random.uniform(18,420),2)
  items.append({'id':f'item{i}','title':TITLES[i%16],'image':image(),'price':price,'old_price':round(price*1.2,2),'condition':random.choice(['New','Pre-owned','Certified refurbished']),'shipping':random.choice(['Free shipping','$6.95 shipping']),'seller':f'quality_finds_{i+1}','rating':random.choice(['99.8%','100%','99.5%']),'bids':random.randint(1,28),'watchers':random.randint(4,230),'selected':i<2,'auction':i%3==0,'status':random.choice(['Active','Sold','Draft']),'quantity':1,'time_left':random.choice(['2h 14m','1d 6h','38m'])})
 return {'page':page,'state':STATES[page][0],'popup_visible':False,'navigation':NAV,'items':items,'active_item':items[0],'categories':CATEGORIES,'viewer':{'name':'Alex Morgan','username':'alex_collects','avatar':image()},'query':'camera','subtotal':round(sum(x['price'] for x in items[:2]),2),'orders':[{'id':f'ORDER-{sample_index:03d}-{i:04d}','item':items[i],'date':f'Sep {20-i}, 2026','status':['Delivered','Shipped','Processing','Return started'][i%4]} for i in range(12)],'chart':[35,52,44,70,62,85,68,92,80,95,75,100],'sample_index':sample_index,'listing_title':TITLES[0],'messages':['Can you share more details about the condition?','Thank you for your interest. The item is in excellent condition.'],'saved_searches':['Vintage cameras','Mechanical keyboards','Trading cards','Leather bags','Automatic watches'],'addresses':[{'name':'Alex Morgan','line':'123 Market Street','city':'San Francisco, CA 94103','country':'United States'}]}
def apply_state(base,state):
 if state not in STATES[base['page']]:raise ValueError(state)
 d=copy.deepcopy(base);d['state']=state;d['popup_visible']=state in POPUPS
 if state=='deals':d['items']=d['items'][::2]
 if state=='filtered':d['items']=[x for x in d['items'] if x['condition']=='New'] or d['items'][:2]
 return d
