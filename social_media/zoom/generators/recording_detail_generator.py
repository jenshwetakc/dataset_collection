from .shared import generate_data,apply_state
RECORDING_DETAIL_STATES=['overview', 'playing', 'paused', 'transcript', 'share_recording_dialog', 'download_panel']
def generate_recording_detail_data(sample_index=0,assets_dir=None):return generate_data('recording_detail',sample_index,assets_dir)
apply_recording_detail_state=apply_state
