from .shared import generate_data, apply_state
MESSAGES_STATES = ('inbox', 'conversation', 'requests', 'new_message', 'chat_details', 'delete_chat')
def generate_messages_data(sample_index=0, assets_dir=None):
    return generate_data('messages', sample_index, assets_dir)
def apply_messages_state(base_data, state):
    return apply_state(base_data, state)
