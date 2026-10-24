from .shared import generate_data,apply_state
FIND_IN_FILES_STATES=['results', 'searching', 'no_results', 'folder_scope', 'replace_preview', 'replace_all_confirm']
def generate_find_in_files_data(sample_index=0,assets_dir=None):return generate_data('find_in_files',sample_index,assets_dir)
apply_find_in_files_state=apply_state
