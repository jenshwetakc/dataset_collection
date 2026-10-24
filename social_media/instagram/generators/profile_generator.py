from .shared import generate_data, apply_state
PROFILE_STATES = ('posts', 'tagged', 'private', 'edit_profile', 'followers', 'profile_options')
def generate_profile_data(sample_index=0, assets_dir=None):
    return generate_data('profile', sample_index, assets_dir)
def apply_profile_state(base_data, state):
    return apply_state(base_data, state)
