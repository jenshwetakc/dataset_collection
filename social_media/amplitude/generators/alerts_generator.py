from .shared import generate_data,apply_state
ALERTS_STATES=['active', 'triggered', 'paused', 'history', 'new_alert', 'alert_menu']
def generate_alerts_data(sample_index=0,assets_dir=None):return generate_data('alerts',sample_index,assets_dir)
apply_alerts_state=apply_state
