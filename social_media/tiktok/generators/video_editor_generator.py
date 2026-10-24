from .shared import generate_data,apply_state
VIDEO_EDITOR_STATES=('trim', 'sounds', 'effects', 'text', 'caption', 'publish_confirmation')
def generate_video_editor_data(sample_index=0,assets_dir=None):
    return generate_data('video_editor',sample_index,assets_dir)
def apply_video_editor_state(base_data,state):
    return apply_state(base_data,state)
