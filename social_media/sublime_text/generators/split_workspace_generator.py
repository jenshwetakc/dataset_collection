from .shared import generate_data,apply_state
SPLIT_WORKSPACE_STATES=['two_columns', 'two_rows', 'four_groups', 'focus_group', 'move_file', 'close_group']
def generate_split_workspace_data(sample_index=0,assets_dir=None):return generate_data('split_workspace',sample_index,assets_dir)
apply_split_workspace_state=apply_state
