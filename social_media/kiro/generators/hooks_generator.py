from .shared import generate_data,apply_state
HOOKS_STATES=['list', 'create', 'editing', 'disabled', 'run_history', 'delete_hook']
def generate_hooks_data(sample_index=0,assets_dir=None):return generate_data('hooks',sample_index,assets_dir)
apply_hooks_state=apply_state
