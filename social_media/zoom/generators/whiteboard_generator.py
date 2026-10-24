from .shared import generate_data,apply_state
WHITEBOARD_STATES=['canvas', 'selected', 'comments', 'presenting', 'board_share_dialog', 'export_panel']
def generate_whiteboard_data(sample_index=0,assets_dir=None):return generate_data('whiteboard',sample_index,assets_dir)
apply_whiteboard_state=apply_state
