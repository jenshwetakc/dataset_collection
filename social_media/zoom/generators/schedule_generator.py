from .shared import generate_data,apply_state
SCHEDULE_STATES=['details', 'recurring', 'advanced', 'invitees', 'schedule_dialog', 'timezone_panel']
def generate_schedule_data(sample_index=0,assets_dir=None):return generate_data('schedule',sample_index,assets_dir)
apply_schedule_state=apply_state
