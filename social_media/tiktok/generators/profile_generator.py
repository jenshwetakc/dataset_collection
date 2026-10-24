from .shared import generate_data,apply_state
PROFILE_STATES=('videos', 'reposts', 'liked', 'private', 'edit_profile', 'followers')
def generate_profile_data(sample_index=0,assets_dir=None):
    return generate_data('profile',sample_index,assets_dir)
def apply_profile_state(base_data,state):
    return apply_state(base_data,state)
