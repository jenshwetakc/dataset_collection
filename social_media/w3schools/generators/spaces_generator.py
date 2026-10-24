from .shared import generate_data,apply_state
SPACES_STATES=('dashboard', 'file_manager', 'editor', 'preview', 'create_space', 'delete_space')
def generate_spaces_data(sample_index=0,assets_dir=None):return generate_data('spaces',sample_index,assets_dir)
def apply_spaces_state(base,state):return apply_state(base,state)
