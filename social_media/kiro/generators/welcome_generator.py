from .shared import generate_data,apply_state
WELCOME_STATES=['start', 'recent', 'empty', 'import_settings', 'open_folder', 'workspace_trust']
def generate_welcome_data(sample_index=0,assets_dir=None):return generate_data('welcome',sample_index,assets_dir)
apply_welcome_state=apply_state
