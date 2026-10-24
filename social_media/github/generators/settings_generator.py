from .shared import generate_data,apply_state
SETTINGS_STATES=('general', 'collaborators', 'branches', 'notifications', 'delete_repository', 'add_secret')
def generate_settings_data(sample_index=0,assets_dir=None):return generate_data('settings',sample_index,assets_dir)
def apply_settings_state(base,state):return apply_state(base,state)
