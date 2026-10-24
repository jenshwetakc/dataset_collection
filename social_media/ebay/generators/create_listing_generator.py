from .shared import generate_data,apply_state
CREATE_LISTING_STATES=('photos', 'item_specifics', 'pricing', 'shipping', 'preview', 'publish_confirmation')
def generate_create_listing_data(sample_index=0,assets_dir=None):
    return generate_data('create_listing',sample_index,assets_dir)
def apply_create_listing_state(base_data,state):
    return apply_state(base_data,state)
