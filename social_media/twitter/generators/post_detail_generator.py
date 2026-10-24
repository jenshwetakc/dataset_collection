from .shared import generate_data,apply_state
POST_DETAIL_STATES=['replies', 'liked', 'reposted', 'reply_dialog', 'share_panel', 'report_dialog']
def generate_post_detail_data(sample_index=0,assets_dir=None):return generate_data('post_detail',sample_index,assets_dir)
apply_post_detail_state=apply_state
