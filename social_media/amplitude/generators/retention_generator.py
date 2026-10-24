from .shared import generate_data,apply_state
RETENTION_STATES=['retention', 'usage_interval', 'cohort_table', 'compare', 'return_event', 'save_cohort']
def generate_retention_data(sample_index=0,assets_dir=None):return generate_data('retention',sample_index,assets_dir)
apply_retention_state=apply_state
