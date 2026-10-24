from .shared import generate_data,apply_state
BOOKMARKS_STATES=['all', 'folder', 'empty', 'folder_picker', 'new_folder', 'clear_dialog']
def generate_bookmarks_data(sample_index=0,assets_dir=None):return generate_data('bookmarks',sample_index,assets_dir)
apply_bookmarks_state=apply_state
