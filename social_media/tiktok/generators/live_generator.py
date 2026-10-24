from .shared import generate_data,apply_state
LIVE_STATES=('watching', 'battle', 'ranking', 'gift_picker', 'viewer_list', 'report')
def generate_live_data(sample_index=0,assets_dir=None):
    return generate_data('live',sample_index,assets_dir)
def apply_live_state(base_data,state):
    return apply_state(base_data,state)
