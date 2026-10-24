from .shared import generate_data,apply_state
FLAG_DETAIL_STATES=['targeting', 'variants', 'activity', 'results', 'rollout_dialog', 'rule_picker']
def generate_flag_detail_data(sample_index=0,assets_dir=None):return generate_data('flag_detail',sample_index,assets_dir)
apply_flag_detail_state=apply_state
