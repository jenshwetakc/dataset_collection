from .shared import generate_data,apply_state
SPACES_STATES=['live', 'upcoming', 'replays', 'following', 'create_space', 'space_filters']
def generate_spaces_data(sample_index=0,assets_dir=None):return generate_data('spaces',sample_index,assets_dir)
apply_spaces_state=apply_state
