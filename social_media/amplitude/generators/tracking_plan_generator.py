from .shared import generate_data,apply_state
TRACKING_PLAN_STATES=['overview', 'validation', 'violations', 'versions', 'new_event', 'publish_dialog']
def generate_tracking_plan_data(sample_index=0,assets_dir=None):return generate_data('tracking_plan',sample_index,assets_dir)
apply_tracking_plan_state=apply_state
