from .shared import generate_data,apply_state
NEW_TAB_STATES=['default', 'private', 'shortcuts_hidden', 'customize_panel', 'typing', 'restore_session']
def generate_new_tab_data(sample_index=0,assets_dir=None):return generate_data('new_tab',sample_index,assets_dir)
apply_new_tab_state=apply_state
