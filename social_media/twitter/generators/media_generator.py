from .shared import generate_data,apply_state
MEDIA_STATES=['photos', 'videos', 'playing', 'paused', 'quality_panel', 'report_dialog']
def generate_media_data(sample_index=0,assets_dir=None):return generate_data('media',sample_index,assets_dir)
apply_media_state=apply_state
