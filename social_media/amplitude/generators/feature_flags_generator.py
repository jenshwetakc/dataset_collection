from .shared import generate_data,apply_state
FEATURE_FLAGS_STATES=['all', 'active', 'inactive', 'archived', 'new_flag', 'flag_menu']
def generate_feature_flags_data(sample_index=0,assets_dir=None):return generate_data('feature_flags',sample_index,assets_dir)
apply_feature_flags_state=apply_state
