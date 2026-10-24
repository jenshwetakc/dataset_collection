from .shared import generate_data,apply_state
LIST_DETAIL_STATES=['timeline', 'members', 'followers', 'edit_list', 'add_members', 'share_panel']
def generate_list_detail_data(sample_index=0,assets_dir=None):return generate_data('list_detail',sample_index,assets_dir)
apply_list_detail_state=apply_state
