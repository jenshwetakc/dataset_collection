from .shared import generate_data,apply_state
ANALYTICS_STATES=['overview', 'posts', 'audience', 'engagement', 'date_panel', 'export_dialog']
def generate_analytics_data(sample_index=0,assets_dir=None):return generate_data('analytics',sample_index,assets_dir)
apply_analytics_state=apply_state
