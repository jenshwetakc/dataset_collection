from .shared import generate_data,apply_state
ENGAGEMENT_STATES=['matrix', 'adoption', 'frequency', 'compare', 'metric_panel', 'save_chart']
def generate_engagement_data(sample_index=0,assets_dir=None):return generate_data('engagement',sample_index,assets_dir)
apply_engagement_state=apply_state
