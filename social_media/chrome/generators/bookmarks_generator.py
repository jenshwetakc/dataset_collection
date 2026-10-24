from .shared import generate_data,apply_state
BOOKMARKS_STATES=('all', 'folder', 'searched', 'empty', 'edit_bookmark', 'new_folder')
def generate_bookmarks_data(sample_index=0,assets_dir=None):return generate_data('bookmarks',sample_index,assets_dir)
def apply_bookmarks_state(base,state):return apply_state(base,state)
