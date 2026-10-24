from .shared import generate_data,apply_state
WEIGHT_STATES=['today', 'trend', 'history', 'empty', 'add_weight', 'weight_goal']
def generate_weight_data(sample_index=0,assets_dir=None):return generate_data('weight',sample_index,assets_dir)
apply_weight_state=apply_state
