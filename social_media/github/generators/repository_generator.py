from .shared import generate_data,apply_state
REPOSITORY_STATES=('code', 'file_view', 'readme', 'releases', 'branch_picker', 'clone')
def generate_repository_data(sample_index=0,assets_dir=None):return generate_data('repository',sample_index,assets_dir)
def apply_repository_state(base,state):return apply_state(base,state)
