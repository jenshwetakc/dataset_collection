from .shared import generate_data,apply_state
COMMUNITY_DETAIL_STATES=['top', 'latest', 'about', 'members', 'join_dialog', 'rules_panel']
def generate_community_detail_data(sample_index=0,assets_dir=None):return generate_data('community_detail',sample_index,assets_dir)
apply_community_detail_state=apply_state
