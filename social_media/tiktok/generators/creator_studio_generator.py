from .shared import generate_data,apply_state
CREATOR_STUDIO_STATES=('overview', 'content', 'audience', 'earnings', 'date_range', 'export')
def generate_creator_studio_data(sample_index=0,assets_dir=None):
    return generate_data('creator_studio',sample_index,assets_dir)
def apply_creator_studio_state(base_data,state):
    return apply_state(base_data,state)
