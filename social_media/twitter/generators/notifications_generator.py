from .shared import generate_data,apply_state
NOTIFICATIONS_STATES=['all', 'verified', 'mentions', 'empty', 'notification_settings', 'push_prompt']
def generate_notifications_data(sample_index=0,assets_dir=None):return generate_data('notifications',sample_index,assets_dir)
apply_notifications_state=apply_state
