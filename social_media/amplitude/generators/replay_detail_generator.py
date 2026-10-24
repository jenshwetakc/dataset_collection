from .shared import generate_data,apply_state
REPLAY_DETAIL_STATES=['paused', 'playing', 'events', 'notes', 'replay_share', 'speed_menu']
def generate_replay_detail_data(sample_index=0,assets_dir=None):return generate_data('replay_detail',sample_index,assets_dir)
apply_replay_detail_state=apply_state
