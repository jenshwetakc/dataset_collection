from .shared import generate_data,apply_state
LIVE_STATES=['latest', 'key_events', 'paused', 'notification_prompt', 'summary_panel', 'ended']
def generate_live_data(sample_index=0,assets_dir=None):return generate_data('live',sample_index,assets_dir)
apply_live_state=apply_state
