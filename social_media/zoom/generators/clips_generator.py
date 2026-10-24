from .shared import generate_data,apply_state
CLIPS_STATES=['all', 'mine', 'shared', 'processing', 'new_clip_dialog', 'clip_menu']
def generate_clips_data(sample_index=0,assets_dir=None):return generate_data('clips',sample_index,assets_dir)
apply_clips_state=apply_state
