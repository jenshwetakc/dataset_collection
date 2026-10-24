from .shared import generate_data,apply_state
SEARCH_RESULTS_STATES=['web', 'images', 'no_results', 'suggestions', 'typing', 'search_settings']
def generate_search_results_data(sample_index=0,assets_dir=None):return generate_data('search_results',sample_index,assets_dir)
apply_search_results_state=apply_state
