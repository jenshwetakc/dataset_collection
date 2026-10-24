from .shared import generate_data,apply_state
WEEKLY_SUMMARY_STATES=['overview', 'activity', 'sleep', 'nutrition', 'share_summary', 'date_panel']
def generate_weekly_summary_data(sample_index=0,assets_dir=None):return generate_data('weekly_summary',sample_index,assets_dir)
apply_weekly_summary_state=apply_state
