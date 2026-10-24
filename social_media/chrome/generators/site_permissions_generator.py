from .shared import generate_data,apply_state
SITE_PERMISSIONS_STATES=('overview', 'camera', 'notifications', 'blocked', 'permission_prompt', 'reset_permissions')
def generate_site_permissions_data(sample_index=0,assets_dir=None):return generate_data('site_permissions',sample_index,assets_dir)
def apply_site_permissions_state(base,state):return apply_state(base,state)
