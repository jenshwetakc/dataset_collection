from .shared import generate_data,apply_state
WORKOUT_HISTORY_STATES=['all', 'walking', 'running', 'empty', 'history_filter', 'export_dialog']
def generate_workout_history_data(sample_index=0,assets_dir=None):return generate_data('workout_history',sample_index,assets_dir)
apply_workout_history_state=apply_state
