from .shared import generate_data,apply_state
REFERENCE_STATES=('index', 'element_detail', 'browser_support', 'filtered', 'copy_example', 'advertisement')
def generate_reference_data(sample_index=0,assets_dir=None):return generate_data('reference',sample_index,assets_dir)
def apply_reference_state(base,state):return apply_state(base,state)
