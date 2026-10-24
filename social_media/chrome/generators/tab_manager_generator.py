from .shared import generate_data,apply_state
TAB_MANAGER_STATES=('grid', 'list', 'grouped', 'incognito_tabs', 'tab_search', 'edit_group')
def generate_tab_manager_data(sample_index=0,assets_dir=None):return generate_data('tab_manager',sample_index,assets_dir)
def apply_tab_manager_state(base,state):return apply_state(base,state)
