from .shared import generate_data,apply_state
ACTIONS_STATES=('runs', 'running', 'failed', 'run_detail', 'dispatch', 'rerun')
def generate_actions_data(sample_index=0,assets_dir=None):return generate_data('actions',sample_index,assets_dir)
def apply_actions_state(base,state):return apply_state(base,state)
