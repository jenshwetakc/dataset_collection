from .shared import generate_data,apply_state
PROJECTS_STATES=('board', 'table', 'roadmap', 'empty', 'new_item', 'field_options')
def generate_projects_data(sample_index=0,assets_dir=None):return generate_data('projects',sample_index,assets_dir)
def apply_projects_state(base,state):return apply_state(base,state)
