from .shared import generate_data,apply_state
REVIEW_STATES=['pending', 'diff', 'accepted', 'rejected', 'tests', 'revert_changes']
def generate_review_data(sample_index=0,assets_dir=None):return generate_data('review',sample_index,assets_dir)
apply_review_state=apply_state
