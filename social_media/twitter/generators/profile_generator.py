from .shared import generate_data,apply_state
PROFILE_STATES=['posts', 'replies', 'highlights', 'media', 'edit_profile', 'profile_menu']
def generate_profile_data(sample_index=0,assets_dir=None):return generate_data('profile',sample_index,assets_dir)
apply_profile_state=apply_state
