from .shared import generate_data,apply_state
PROJECT_SETTINGS_STATES=['general', 'access', 'ingestion', 'privacy', 'project_dialog', 'key_panel']
def generate_project_settings_data(sample_index=0,assets_dir=None):return generate_data('project_settings',sample_index,assets_dir)
apply_project_settings_state=apply_state
