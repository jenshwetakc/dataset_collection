from .shared import generate_data,apply_state
HISTORY_STATES=['all', 'searched', 'empty', 'sidebar', 'delete_selected', 'clear_history']
def generate_history_data(sample_index=0,assets_dir=None):return generate_data('history',sample_index,assets_dir)
apply_history_state=apply_state
