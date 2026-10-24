from .shared import generate_data,apply_state
EXTENSIONS_STATES=('installed', 'developer_mode', 'empty', 'disabled', 'extension_details', 'remove_extension')
def generate_extensions_data(sample_index=0,assets_dir=None):return generate_data('extensions',sample_index,assets_dir)
def apply_extensions_state(base,state):return apply_state(base,state)
