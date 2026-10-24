from .shared import generate_data,apply_state
TRYIT_EDITOR_STATES=('html', 'css', 'javascript', 'console_error', 'save_code', 'advertisement')
def generate_tryit_editor_data(sample_index=0,assets_dir=None):return generate_data('tryit_editor',sample_index,assets_dir)
def apply_tryit_editor_state(base,state):return apply_state(base,state)
