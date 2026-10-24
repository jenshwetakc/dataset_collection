from .shared import generate_data,apply_state
CART_STATES=('filled', 'saved_for_later', 'price_changed', 'empty', 'remove_item', 'shipping_options')
def generate_cart_data(sample_index=0,assets_dir=None):
    return generate_data('cart',sample_index,assets_dir)
def apply_cart_state(base_data,state):
    return apply_state(base_data,state)
