from .shared import generate_data,apply_state
NOTEBOOK_STATES=['editing', 'executed', 'running', 'error', 'split', 'restart_kernel']
def generate_notebook_data(sample_index=0,assets_dir=None):return generate_data('notebook',sample_index,assets_dir)
apply_notebook_state=apply_state
