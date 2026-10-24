from .shared import generate_data,apply_state
EXERCISE_LIBRARY_STATES=['favorites', 'all', 'searching', 'recent', 'exercise_settings', 'add_favorite']
def generate_exercise_library_data(sample_index=0,assets_dir=None):return generate_data('exercise_library',sample_index,assets_dir)
apply_exercise_library_state=apply_state
