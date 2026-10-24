from .shared import generate_data,apply_state
TAB_MANAGER_STATES=['grid', 'list', 'vertical_tabs', 'private_tabs', 'tab_menu', 'close_all']
def generate_tab_manager_data(sample_index=0,assets_dir=None):return generate_data('tab_manager',sample_index,assets_dir)
apply_tab_manager_state=apply_state
