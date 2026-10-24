from .shared import generate_data,apply_state
TITLE_DETAIL_STATES=('overview', 'episodes', 'more_like_this', 'trailers', 'rating', 'share')
def generate_title_detail_data(sample_index=0,assets_dir=None):return generate_data('title_detail',sample_index,assets_dir)
def apply_title_detail_state(base,state):return apply_state(base,state)
