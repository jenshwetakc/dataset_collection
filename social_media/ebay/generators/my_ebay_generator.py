from .shared import generate_data,apply_state
MY_EBAY_STATES=('summary', 'watchlist', 'saved_searches', 'saved_sellers', 'collection', 'watchlist_actions')
def generate_my_ebay_data(sample_index=0,assets_dir=None):
    return generate_data('my_ebay',sample_index,assets_dir)
def apply_my_ebay_state(base_data,state):
    return apply_state(base_data,state)
