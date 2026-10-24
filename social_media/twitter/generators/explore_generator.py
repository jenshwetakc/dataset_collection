from .shared import generate_data,apply_state
EXPLORE_STATES=['trending', 'news', 'sports', 'entertainment', 'location_panel', 'cookie_corner']
def generate_explore_data(sample_index=0,assets_dir=None):return generate_data('explore',sample_index,assets_dir)
apply_explore_state=apply_state
