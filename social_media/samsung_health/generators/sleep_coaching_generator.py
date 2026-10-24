from .shared import generate_data,apply_state
SLEEP_COACHING_STATES=['overview', 'tasks', 'history', 'not_started', 'start_coaching', 'coaching_reminder']
def generate_sleep_coaching_data(sample_index=0,assets_dir=None):return generate_data('sleep_coaching',sample_index,assets_dir)
apply_sleep_coaching_state=apply_state
