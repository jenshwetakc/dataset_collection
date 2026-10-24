from .shared import generate_data,apply_state
WORKOUT_SUMMARY_STATES=['overview', 'splits', 'heart_rate', 'photos', 'share_workout', 'delete_record']
def generate_workout_summary_data(sample_index=0,assets_dir=None):return generate_data('workout_summary',sample_index,assets_dir)
apply_workout_summary_state=apply_state
