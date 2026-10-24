from .shared import generate_data,apply_state
COHORT_DETAIL_STATES=['definition', 'users', 'growth', 'syncs', 'condition_picker', 'sync_dialog']
def generate_cohort_detail_data(sample_index=0,assets_dir=None):return generate_data('cohort_detail',sample_index,assets_dir)
apply_cohort_detail_state=apply_state
