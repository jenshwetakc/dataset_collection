from .shared import generate_data, apply_state
REELS_STATES = ('playing', 'paused', 'muted', 'comments', 'share', 'report')
def generate_reels_data(sample_index=0, assets_dir=None):
    return generate_data('reels', sample_index, assets_dir)
def apply_reels_state(base_data, state):
    return apply_state(base_data, state)
