from .shared import generate_data,apply_state
WORKOUT_LIVE_STATES=['running', 'paused', 'locked', 'gps_searching', 'finish_workout', 'audio_panel']
def generate_workout_live_data(sample_index=0,assets_dir=None):return generate_data('workout_live',sample_index,assets_dir)
apply_workout_live_state=apply_state
