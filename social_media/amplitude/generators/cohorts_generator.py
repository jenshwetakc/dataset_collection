from .shared import generate_data,apply_state
COHORTS_STATES=['all', 'owned', 'shared', 'archived', 'new_cohort', 'cohort_menu']
def generate_cohorts_data(sample_index=0,assets_dir=None):return generate_data('cohorts',sample_index,assets_dir)
apply_cohorts_state=apply_state
