from .shared import generate_data, apply_state
CREATE_STATES = ('upload', 'crop', 'filters', 'caption', 'discard', 'published')
def generate_create_data(sample_index=0, assets_dir=None):
    return generate_data('create', sample_index, assets_dir)
def apply_create_state(base_data, state):
    return apply_state(base_data, state)
