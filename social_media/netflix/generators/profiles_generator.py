from .shared import generate_data,apply_state
PROFILES_STATES=('choose', 'manage', 'edit', 'add', 'profile_lock', 'delete_profile')
def generate_profiles_data(sample_index=0,assets_dir=None):return generate_data('profiles',sample_index,assets_dir)
def apply_profiles_state(base,state):return apply_state(base,state)
