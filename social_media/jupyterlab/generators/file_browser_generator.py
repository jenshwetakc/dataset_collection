from .shared import generate_data,apply_state
FILE_BROWSER_STATES=['list', 'selected', 'searching', 'empty', 'rename', 'delete_files']
def generate_file_browser_data(sample_index=0,assets_dir=None):return generate_data('file_browser',sample_index,assets_dir)
apply_file_browser_state=apply_state
