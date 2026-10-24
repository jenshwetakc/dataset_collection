from .shared import generate_data, apply_state
NOTIFICATIONS_STATES = ('all', 'mentions', 'requests', 'following', 'notification_options', 'remove_notification')
def generate_notifications_data(sample_index=0, assets_dir=None):
    return generate_data('notifications', sample_index, assets_dir)
def apply_notifications_state(base_data, state):
    return apply_state(base_data, state)
