from .shared import generate_data,apply_state
CHECKOUT_STATES=('review', 'address', 'payment', 'coupon_applied', 'address_dialog', 'order_confirmation')
def generate_checkout_data(sample_index=0,assets_dir=None):
    return generate_data('checkout',sample_index,assets_dir)
def apply_checkout_state(base_data,state):
    return apply_state(base_data,state)
