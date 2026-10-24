from .shared import generate_data,apply_state
CODE_EDITOR_STATES=['editing', 'split_editor', 'completion', 'inspection', 'rename_symbol', 'find_in_files']
def generate_code_editor_data(sample_index=0,assets_dir=None):return generate_data('code_editor',sample_index,assets_dir)
apply_code_editor_state=apply_state
