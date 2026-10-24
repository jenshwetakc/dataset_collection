from .shared import generate_data,apply_state
ENERGY_SCORE_STATES=['today', 'week', 'factors', 'no_data', 'score_info', 'connect_device']
def generate_energy_score_data(sample_index=0,assets_dir=None):return generate_data('energy_score',sample_index,assets_dir)
apply_energy_score_state=apply_state
