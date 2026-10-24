from .shared import generate_data,apply_state
ISSUE_DETAIL_STATES=('open', 'closed', 'editing', 'tasklist', 'assign', 'close_issue')
def generate_issue_detail_data(sample_index=0,assets_dir=None):return generate_data('issue_detail',sample_index,assets_dir)
def apply_issue_detail_state(base,state):return apply_state(base,state)
