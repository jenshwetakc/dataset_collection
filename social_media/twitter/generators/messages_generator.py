from .shared import generate_data,apply_state
MESSAGES_STATES=['inbox', 'requests', 'archived', 'empty', 'new_message', 'message_settings']
def generate_messages_data(sample_index=0,assets_dir=None):return generate_data('messages',sample_index,assets_dir)
apply_messages_state=apply_state
