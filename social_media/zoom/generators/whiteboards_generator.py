from .shared import generate_data,apply_state
WHITEBOARDS_STATES=['recent', 'owned', 'shared', 'templates', 'new_board_dialog', 'board_menu']
def generate_whiteboards_data(sample_index=0,assets_dir=None):return generate_data('whiteboards',sample_index,assets_dir)
apply_whiteboards_state=apply_state
