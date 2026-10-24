from .shared import generate_data,apply_state
MEETINGS_STATES=['upcoming', 'previous', 'personal_room', 'empty', 'meeting_menu', 'delete_dialog']
def generate_meetings_data(sample_index=0,assets_dir=None):return generate_data('meetings',sample_index,assets_dir)
apply_meetings_state=apply_state
