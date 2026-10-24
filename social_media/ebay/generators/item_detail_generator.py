from .shared import generate_data,apply_state
ITEM_DETAIL_STATES=('buy_now', 'variations', 'auction', 'out_of_stock', 'image_gallery', 'contact_seller')
def generate_item_detail_data(sample_index=0,assets_dir=None):
    return generate_data('item_detail',sample_index,assets_dir)
def apply_item_detail_state(base_data,state):
    return apply_state(base_data,state)
