from .shared import generate_data,apply_state
SCREEN_SHARE_STATES=['desktop', 'window', 'whiteboard', 'sharing', 'share_options', 'stop_share_dialog']
def generate_screen_share_data(sample_index=0,assets_dir=None):return generate_data('screen_share',sample_index,assets_dir)
apply_screen_share_state=apply_state
