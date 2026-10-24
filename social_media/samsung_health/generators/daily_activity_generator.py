from .shared import generate_data,apply_state
DAILY_ACTIVITY_STATES=['today', 'week', 'month', 'goal_reached', 'activity_goal', 'date_panel']
def generate_daily_activity_data(sample_index=0,assets_dir=None):return generate_data('daily_activity',sample_index,assets_dir)
apply_daily_activity_state=apply_state
