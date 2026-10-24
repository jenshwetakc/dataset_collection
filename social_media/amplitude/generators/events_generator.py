from .shared import generate_data,apply_state
EVENTS_STATES=['catalog', 'live', 'hidden', 'unplanned', 'event_schema', 'event_menu']
def generate_events_data(sample_index=0,assets_dir=None):return generate_data('events',sample_index,assets_dir)
apply_events_state=apply_state
