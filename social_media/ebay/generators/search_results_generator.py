from .shared import generate_data,apply_state
SEARCH_RESULTS_STATES=('grid', 'list', 'filtered', 'no_results', 'filter_dialog', 'sort_menu')
def generate_search_results_data(sample_index=0,assets_dir=None):
    return generate_data('search_results',sample_index,assets_dir)
def apply_search_results_state(base_data,state):
    return apply_state(base_data,state)
