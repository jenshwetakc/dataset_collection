from .shared import generate_data, apply_state
STORIES_STATES = ('viewing', 'paused', 'reply', 'viewers', 'share', 'story_options')
def generate_stories_data(sample_index=0, assets_dir=None):
    return generate_data('stories', sample_index, assets_dir)
def apply_stories_state(base_data, state):
    return apply_state(base_data, state)
