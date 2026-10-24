from .shared import generate_data,apply_state
CALENDAR_STATES=['week', 'day', 'agenda', 'month', 'event_panel', 'calendar_connect_dialog']
def generate_calendar_data(sample_index=0,assets_dir=None):return generate_data('calendar',sample_index,assets_dir)
apply_calendar_state=apply_state
