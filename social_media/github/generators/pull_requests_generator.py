from .shared import generate_data,apply_state
PULL_REQUESTS_STATES=('open', 'closed', 'drafts', 'empty', 'compare_branches', 'filters')
def generate_pull_requests_data(sample_index=0,assets_dir=None):return generate_data('pull_requests',sample_index,assets_dir)
def apply_pull_requests_state(base,state):return apply_state(base,state)
