from .shared import generate_data,apply_state
FOR_YOU_STATES=('playing', 'paused', 'following', 'friends', 'comments', 'share')
def generate_for_you_data(sample_index=0,assets_dir=None):
    return generate_data('for_you',sample_index,assets_dir)
def apply_for_you_state(base_data,state):
    return apply_state(base_data,state)
