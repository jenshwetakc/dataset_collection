from .shared import generate_data,apply_state
LAYOUT_EDITOR_STATES=['design', 'blueprint', 'split', 'constraint_warning', 'attributes', 'add_component']
def generate_layout_editor_data(sample_index=0,assets_dir=None):return generate_data('layout_editor',sample_index,assets_dir)
apply_layout_editor_state=apply_state
