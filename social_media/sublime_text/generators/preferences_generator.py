from .shared import generate_data,apply_state
PREFERENCES_STATES=['settings', 'key_bindings', 'color_scheme', 'theme', 'invalid_json', 'reset_settings']
def generate_preferences_data(sample_index=0,assets_dir=None):return generate_data('preferences',sample_index,assets_dir)
apply_preferences_state=apply_state
