from .shared import generate_data,apply_state
BODY_COMPOSITION_STATES=['latest', 'trend', 'history', 'no_data', 'body_goal', 'measure_guide']
def generate_body_composition_data(sample_index=0,assets_dir=None):return generate_data('body_composition',sample_index,assets_dir)
apply_body_composition_state=apply_state
