from .shared import generate_data, apply_state
EXPLORE_STATES = ('discover', 'search_results', 'accounts', 'tags', 'post_detail', 'search_filters')
def generate_explore_data(sample_index=0, assets_dir=None):
    return generate_data('explore', sample_index, assets_dir)
def apply_explore_state(base_data, state):
    return apply_state(base_data, state)
