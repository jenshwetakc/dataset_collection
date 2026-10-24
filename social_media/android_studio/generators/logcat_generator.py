from .shared import generate_data,apply_state
LOGCAT_STATES=['streaming', 'paused', 'errors', 'no_device', 'filtered', 'save_filter']
def generate_logcat_data(sample_index=0,assets_dir=None):return generate_data('logcat',sample_index,assets_dir)
apply_logcat_state=apply_state
