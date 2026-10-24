from .shared import generate_data,apply_state
EXTENSIONS_STATES=['discover', 'installed', 'details', 'disabled', 'install_confirm', 'uninstall_confirm']
def generate_extensions_data(sample_index=0,assets_dir=None):return generate_data('extensions',sample_index,assets_dir)
apply_extensions_state=apply_state
