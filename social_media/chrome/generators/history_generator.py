from .shared import generate_data,apply_state
HISTORY_STATES=('all', 'searched', 'selected', 'empty', 'delete_selected', 'clear_data')
def generate_history_data(sample_index=0,assets_dir=None):return generate_data('history',sample_index,assets_dir)
def apply_history_state(base,state):return apply_state(base,state)
