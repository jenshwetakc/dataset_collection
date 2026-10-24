from .shared import generate_data,apply_state
SLEEP_STATES=['last_night', 'week', 'stages', 'no_data', 'sleep_time', 'sleep_settings']
def generate_sleep_data(sample_index=0,assets_dir=None):return generate_data('sleep',sample_index,assets_dir)
apply_sleep_state=apply_state
