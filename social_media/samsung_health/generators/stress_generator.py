from .shared import generate_data,apply_state
STRESS_STATES=['latest', 'week', 'breathing', 'no_data', 'breathing_settings', 'stress_info']
def generate_stress_data(sample_index=0,assets_dir=None):return generate_data('stress',sample_index,assets_dir)
apply_stress_state=apply_state
