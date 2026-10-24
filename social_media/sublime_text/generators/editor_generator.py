from .shared import generate_data,apply_state
EDITOR_STATES=['editing', 'selection', 'multiple_cursors', 'autocomplete', 'unsaved', 'save_as']
def generate_editor_data(sample_index=0,assets_dir=None):return generate_data('editor',sample_index,assets_dir)
apply_editor_state=apply_state
