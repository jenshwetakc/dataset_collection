from .shared import generate_data,apply_state
HEART_RATE_STATES=['latest', 'week', 'resting', 'no_data', 'measurement_dialog', 'heart_rate_settings']
def generate_heart_rate_data(sample_index=0,assets_dir=None):return generate_data('heart_rate',sample_index,assets_dir)
apply_heart_rate_state=apply_state
