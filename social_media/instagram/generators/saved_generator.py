from .shared import generate_data, apply_state
SAVED_STATES = ('collections', 'all_posts', 'collection_detail', 'new_collection', 'edit_collection', 'delete_collection')
def generate_saved_data(sample_index=0, assets_dir=None):
    return generate_data('saved', sample_index, assets_dir)
def apply_saved_state(base_data, state):
    return apply_state(base_data, state)
