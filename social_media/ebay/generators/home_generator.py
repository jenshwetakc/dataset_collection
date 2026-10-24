from .shared import generate_data,apply_state
HOME_STATES=('recommended', 'deals', 'recently_viewed', 'categories', 'category_menu', 'notifications')
def generate_home_data(sample_index=0,assets_dir=None):
    return generate_data('home',sample_index,assets_dir)
def apply_home_state(base_data,state):
    return apply_state(base_data,state)
