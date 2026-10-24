from .shared import generate_data,apply_state
NEW_TAB_STATES=('default', 'shortcuts_hidden', 'custom_background', 'incognito', 'customize', 'add_shortcut')
def generate_new_tab_data(sample_index=0,assets_dir=None):return generate_data('new_tab',sample_index,assets_dir)
def apply_new_tab_state(base,state):return apply_state(base,state)
