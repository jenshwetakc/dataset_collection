from .shared import generate_data,apply_state
SOUND_STATES=('overview', 'popular', 'recent', 'saved', 'use_sound', 'sound_options')
def generate_sound_data(sample_index=0,assets_dir=None):
    return generate_data('sound',sample_index,assets_dir)
def apply_sound_state(base_data,state):
    return apply_state(base_data,state)
