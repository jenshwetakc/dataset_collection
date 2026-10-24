from .shared import generate_data,apply_state
DEVICE_MANAGER_STATES=['virtual_devices', 'running', 'physical', 'downloading', 'create_device', 'delete_device']
def generate_device_manager_data(sample_index=0,assets_dir=None):return generate_data('device_manager',sample_index,assets_dir)
apply_device_manager_state=apply_state
