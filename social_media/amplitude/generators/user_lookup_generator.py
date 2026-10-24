from .shared import generate_data,apply_state
USER_LOOKUP_STATES=['all', 'active', 'searching', 'empty', 'user_filter', 'export_dialog']
def generate_user_lookup_data(sample_index=0,assets_dir=None):return generate_data('user_lookup',sample_index,assets_dir)
apply_user_lookup_state=apply_state
