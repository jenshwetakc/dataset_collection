from .shared import generate_data,apply_state
INBOX_STATES=('activity', 'messages', 'requests', 'conversation', 'new_message', 'notification_options')
def generate_inbox_data(sample_index=0,assets_dir=None):
    return generate_data('inbox',sample_index,assets_dir)
def apply_inbox_state(base_data,state):
    return apply_state(base_data,state)
