from .shared import generate_data,apply_state
SPACE_DETAIL_STATES=['listening', 'speaking', 'muted', 'participants_panel', 'leave_dialog', 'share_panel']
def generate_space_detail_data(sample_index=0,assets_dir=None):return generate_data('space_detail',sample_index,assets_dir)
apply_space_detail_state=apply_state
