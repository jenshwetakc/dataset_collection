from .shared import generate_data,apply_state
SHIELDS_STATES=['standard', 'strict', 'custom', 'tracking_panel', 'site_permissions', 'clear_data']
def generate_shields_data(sample_index=0,assets_dir=None):return generate_data('shields',sample_index,assets_dir)
apply_shields_state=apply_state
