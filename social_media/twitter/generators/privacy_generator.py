from .shared import generate_data,apply_state
PRIVACY_STATES=['audience', 'messages', 'discoverability', 'muted', 'cookie_preferences', 'data_dialog']
def generate_privacy_data(sample_index=0,assets_dir=None):return generate_data('privacy',sample_index,assets_dir)
apply_privacy_state=apply_state
