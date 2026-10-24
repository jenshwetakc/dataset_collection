from .shared import generate_data,apply_state
RECORDINGS_STATES=['cloud', 'computer', 'processing', 'trash', 'recording_menu', 'delete_dialog']
def generate_recordings_data(sample_index=0,assets_dir=None):return generate_data('recordings',sample_index,assets_dir)
apply_recordings_state=apply_state
