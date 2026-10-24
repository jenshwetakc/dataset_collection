from .shared import generate_data,apply_state
PROJECT_STATES=['tree', 'collapsed', 'open_files', 'empty', 'rename', 'new_file']
def generate_project_data(sample_index=0,assets_dir=None):return generate_data('project',sample_index,assets_dir)
apply_project_state=apply_state
