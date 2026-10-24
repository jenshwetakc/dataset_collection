from .shared import generate_data,apply_state
SELLER_HUB_STATES=('overview', 'active_listings', 'sold', 'drafts', 'bulk_edit', 'promote_listing')
def generate_seller_hub_data(sample_index=0,assets_dir=None):
    return generate_data('seller_hub',sample_index,assets_dir)
def apply_seller_hub_state(base_data,state):
    return apply_state(base_data,state)
