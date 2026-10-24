from .shared import generate_data, apply_state
SETTINGS_STATES = ('account', 'privacy', 'notifications', 'security', 'logout', 'delete_account')
def generate_settings_data(sample_index=0, assets_dir=None):
    return generate_data('settings', sample_index, assets_dir)
def apply_settings_state(base_data, state):
    return apply_state(base_data, state)
