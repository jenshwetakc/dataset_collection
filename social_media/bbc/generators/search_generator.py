from .shared import generate_data,apply_state
SEARCH_STATES=['results', 'typing', 'filtered', 'no_results', 'filter_panel', 'saved_search_dialog']
def generate_search_data(sample_index=0,assets_dir=None):return generate_data('search',sample_index,assets_dir)
apply_search_state=apply_state
