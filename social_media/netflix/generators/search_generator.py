from .shared import generate_data,apply_state
SEARCH_STATES=('suggested', 'results', 'no_results', 'genre_results', 'filters', 'voice_search')
def generate_search_data(sample_index=0,assets_dir=None):return generate_data('search',sample_index,assets_dir)
def apply_search_state(base,state):return apply_state(base,state)
