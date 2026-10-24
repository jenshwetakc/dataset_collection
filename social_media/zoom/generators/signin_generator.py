from .shared import generate_data,apply_state
SIGNIN_STATES=['email', 'password', 'error', 'sso', 'help_dialog', 'cookie_corner']
def generate_signin_data(sample_index=0,assets_dir=None):return generate_data('signin',sample_index,assets_dir)
apply_signin_state=apply_state
