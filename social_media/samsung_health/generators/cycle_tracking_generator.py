from .shared import generate_data,apply_state
CYCLE_TRACKING_STATES=['calendar', 'history', 'symptoms', 'not_started', 'log_cycle', 'cycle_privacy']
def generate_cycle_tracking_data(sample_index=0,assets_dir=None):return generate_data('cycle_tracking',sample_index,assets_dir)
apply_cycle_tracking_state=apply_state
