from .shared import generate_data,apply_state
ACCOUNT_STATES=('dashboard', 'profile', 'progress', 'preferences', 'sign_in', 'cookie_preferences')
def generate_account_data(sample_index=0,assets_dir=None):return generate_data('account',sample_index,assets_dir)
def apply_account_state(base,state):return apply_state(base,state)
