from .shared import generate_data,apply_state
PRIVACY_STATES=['standard', 'strict', 'custom', 'tracking_panel', 'site_permissions', 'clear_data']
def generate_privacy_data(sample_index=0,assets_dir=None):return generate_data('privacy',sample_index,assets_dir)
apply_privacy_state=apply_state
