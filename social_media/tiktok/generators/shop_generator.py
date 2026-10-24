from .shared import generate_data,apply_state
SHOP_STATES=('recommended', 'category', 'product_detail', 'cart', 'checkout', 'order_success')
def generate_shop_data(sample_index=0,assets_dir=None):
    return generate_data('shop',sample_index,assets_dir)
def apply_shop_state(base_data,state):
    return apply_state(base_data,state)
