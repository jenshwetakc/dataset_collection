from .shared import generate_data,apply_state
ACCOUNT_STATES=('overview', 'membership', 'devices', 'playback_settings', 'change_plan', 'sign_out_devices')
def generate_account_data(sample_index=0,assets_dir=None):return generate_data('account',sample_index,assets_dir)
def apply_account_state(base,state):return apply_state(base,state)
