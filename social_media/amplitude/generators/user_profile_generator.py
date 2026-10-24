from .shared import generate_data,apply_state
USER_PROFILE_STATES=['activity', 'properties', 'sessions', 'cohorts', 'event_detail', 'delete_user']
def generate_user_profile_data(sample_index=0,assets_dir=None):return generate_data('user_profile',sample_index,assets_dir)
apply_user_profile_state=apply_state
