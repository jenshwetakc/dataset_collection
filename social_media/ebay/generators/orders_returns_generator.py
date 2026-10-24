from .shared import generate_data,apply_state
ORDERS_RETURNS_STATES=('purchases', 'order_detail', 'tracking', 'return_details', 'start_return', 'leave_feedback')
def generate_orders_returns_data(sample_index=0,assets_dir=None):
    return generate_data('orders_returns',sample_index,assets_dir)
def apply_orders_returns_state(base_data,state):
    return apply_state(base_data,state)
