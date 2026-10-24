from .shared import generate_data,apply_state
CODE_SEARCH_STATES=('code', 'repositories', 'users', 'no_results', 'advanced_filters', 'saved_search')
def generate_code_search_data(sample_index=0,assets_dir=None):return generate_data('code_search',sample_index,assets_dir)
def apply_code_search_state(base,state):return apply_state(base,state)
