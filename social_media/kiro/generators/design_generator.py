from .shared import generate_data,apply_state
DESIGN_STATES=['overview', 'architecture', 'interfaces', 'data_model', 'alternatives', 'regenerate_design']
def generate_design_data(sample_index=0,assets_dir=None):return generate_data('design',sample_index,assets_dir)
apply_design_state=apply_state
