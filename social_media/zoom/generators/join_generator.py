from .shared import generate_data,apply_state
JOIN_STATES=['meeting_id', 'personal_link', 'connecting', 'invalid_id', 'permission_panel', 'passcode_dialog']
def generate_join_data(sample_index=0,assets_dir=None):return generate_data('join',sample_index,assets_dir)
apply_join_state=apply_state
