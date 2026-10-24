from .shared import generate_data,apply_state
HOME_STATES=('landing', 'search_results', 'learning_paths', 'signed_in', 'tutorial_menu', 'advertisement')
def generate_home_data(sample_index=0,assets_dir=None):return generate_data('home',sample_index,assets_dir)
def apply_home_state(base,state):return apply_state(base,state)
