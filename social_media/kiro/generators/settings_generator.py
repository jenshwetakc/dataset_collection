from .shared import generate_data,apply_state
SETTINGS_STATES=['general', 'appearance', 'editor', 'privacy', 'account', 'reset_settings']
def generate_settings_data(sample_index=0,assets_dir=None):return generate_data('settings',sample_index,assets_dir)
apply_settings_state=apply_state
