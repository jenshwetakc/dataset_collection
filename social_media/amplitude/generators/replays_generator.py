from .shared import generate_data,apply_state
REPLAYS_STATES=['all', 'errors', 'rage_clicks', 'favorites', 'replay_filter', 'privacy_panel']
def generate_replays_data(sample_index=0,assets_dir=None):return generate_data('replays',sample_index,assets_dir)
apply_replays_state=apply_state
