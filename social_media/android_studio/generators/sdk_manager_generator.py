from .shared import generate_data,apply_state
SDK_MANAGER_STATES=['platforms', 'tools', 'updates', 'installing', 'license_dialog', 'apply_changes']
def generate_sdk_manager_data(sample_index=0,assets_dir=None):return generate_data('sdk_manager',sample_index,assets_dir)
apply_sdk_manager_state=apply_state
