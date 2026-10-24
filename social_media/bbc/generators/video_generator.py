from .shared import generate_data,apply_state
VIDEO_STATES=['featured', 'playing', 'paused', 'captions', 'quality_menu', 'consent_dialog']
def generate_video_data(sample_index=0,assets_dir=None):return generate_data('video',sample_index,assets_dir)
apply_video_state=apply_state
