from .shared import generate_data,apply_state
MEETING_STATES=['gallery', 'speaker', 'muted', 'video_off', 'reactions_panel', 'end_dialog']
def generate_meeting_data(sample_index=0,assets_dir=None):return generate_data('meeting',sample_index,assets_dir)
apply_meeting_state=apply_state
