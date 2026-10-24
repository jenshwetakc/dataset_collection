from .shared import generate_data,apply_state
PACKAGE_CONTROL_STATES=['installed', 'discover', 'details', 'disabled', 'install_confirm', 'remove_confirm']
def generate_package_control_data(sample_index=0,assets_dir=None):return generate_data('package_control',sample_index,assets_dir)
apply_package_control_state=apply_state
