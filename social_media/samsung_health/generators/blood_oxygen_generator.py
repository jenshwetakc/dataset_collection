from .shared import generate_data,apply_state
BLOOD_OXYGEN_STATES=['latest', 'sleep', 'history', 'no_data', 'oxygen_info', 'connect_device']
def generate_blood_oxygen_data(sample_index=0,assets_dir=None):return generate_data('blood_oxygen',sample_index,assets_dir)
apply_blood_oxygen_state=apply_state
