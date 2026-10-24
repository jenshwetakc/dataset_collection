from .shared import generate_data,apply_state
HOME_STATES=['overview', 'upcoming', 'cookie_banner', 'cookie_corner', 'quick_menu', 'sponsor_panel']
def generate_home_data(sample_index=0,assets_dir=None):return generate_data('home',sample_index,assets_dir)
apply_home_state=apply_state
