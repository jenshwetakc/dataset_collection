from .shared import generate_data,apply_state
PULL_REQUEST_DETAIL_STATES=('conversation', 'commits', 'files_changed', 'checks', 'review', 'merge')
def generate_pull_request_detail_data(sample_index=0,assets_dir=None):return generate_data('pull_request_detail',sample_index,assets_dir)
def apply_pull_request_detail_state(base,state):return apply_state(base,state)
