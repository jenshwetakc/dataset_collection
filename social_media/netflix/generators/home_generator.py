from .shared import generate_data,apply_state
HOME_STATES=('recommended', 'tv_shows', 'movies', 'continue_watching', 'notifications', 'category_picker')
def generate_home_data(sample_index=0,assets_dir=None):return generate_data('home',sample_index,assets_dir)
def apply_home_state(base,state):return apply_state(base,state)
