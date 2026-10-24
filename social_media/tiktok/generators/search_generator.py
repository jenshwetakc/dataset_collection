from .shared import generate_data,apply_state
SEARCH_STATES=('top', 'videos', 'users', 'sounds', 'hashtags', 'filters')
def generate_search_data(sample_index=0,assets_dir=None):
    return generate_data('search',sample_index,assets_dir)
def apply_search_state(base_data,state):
    return apply_state(base_data,state)
