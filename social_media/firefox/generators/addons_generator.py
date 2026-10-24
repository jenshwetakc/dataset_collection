from .shared import generate_data, apply_state

ADDONS_STATES = ['extensions', 'themes', 'disabled', 'details', 'addon_menu', 'remove_addon']


def generate_addons_data(sample_index=0, assets_dir=None): return generate_data('addons', sample_index, assets_dir)


apply_addons_state = apply_state
