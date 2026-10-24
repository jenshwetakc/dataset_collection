from .shared import generate_data,apply_state
ISSUES_STATES=('open', 'closed', 'filtered', 'empty', 'labels', 'new_issue')
def generate_issues_data(sample_index=0,assets_dir=None):return generate_data('issues',sample_index,assets_dir)
def apply_issues_state(base,state):return apply_state(base,state)
