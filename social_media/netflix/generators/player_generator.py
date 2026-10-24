from .shared import generate_data,apply_state
PLAYER_STATES=('playing', 'paused', 'buffering', 'episode_end', 'audio_subtitles', 'playback_error')
def generate_player_data(sample_index=0,assets_dir=None):return generate_data('player',sample_index,assets_dir)
def apply_player_state(base,state):return apply_state(base,state)
