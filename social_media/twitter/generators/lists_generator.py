from .shared import generate_data,apply_state
LISTS_STATES=['discover', 'yours', 'pinned', 'member_of', 'new_list', 'list_menu']
def generate_lists_data(sample_index=0,assets_dir=None):return generate_data('lists',sample_index,assets_dir)
apply_lists_state=apply_state
