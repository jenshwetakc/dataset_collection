from .shared import generate_data,apply_state
SEARCH_STATES=['top', 'latest', 'people', 'media', 'typing', 'filter_panel']
def generate_search_data(sample_index=0,assets_dir=None):return generate_data('search',sample_index,assets_dir)
apply_search_state=apply_state
