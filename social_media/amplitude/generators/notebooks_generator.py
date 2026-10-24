from .shared import generate_data,apply_state
NOTEBOOKS_STATES=['all', 'owned', 'shared', 'templates', 'new_notebook', 'notebook_share']
def generate_notebooks_data(sample_index=0,assets_dir=None):return generate_data('notebooks',sample_index,assets_dir)
apply_notebooks_state=apply_state
