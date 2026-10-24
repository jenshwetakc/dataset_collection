from .shared import generate_data,apply_state
LOGIN_STATES=['identifier', 'password', 'error', 'two_factor', 'help_dialog', 'cookie_banner']
def generate_login_data(sample_index=0,assets_dir=None):return generate_data('login',sample_index,assets_dir)
apply_login_state=apply_state
