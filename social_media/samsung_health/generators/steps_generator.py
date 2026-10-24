from .shared import generate_data,apply_state
STEPS_STATES=['today', 'week', 'month', 'paused', 'step_goal', 'source_panel']
def generate_steps_data(sample_index=0,assets_dir=None):return generate_data('steps',sample_index,assets_dir)
apply_steps_state=apply_state
