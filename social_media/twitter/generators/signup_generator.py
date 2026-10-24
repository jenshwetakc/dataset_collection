from .shared import generate_data,apply_state
SIGNUP_STATES=['details', 'customize', 'verification', 'password', 'terms_dialog', 'cookie_corner']
def generate_signup_data(sample_index=0,assets_dir=None):return generate_data('signup',sample_index,assets_dir)
apply_signup_state=apply_state
