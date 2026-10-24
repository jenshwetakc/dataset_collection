from .shared import generate_data,apply_state
MEETING_CHAT_STATES=['everyone', 'direct', 'file', 'typing', 'chat_menu', 'save_chat_dialog']
def generate_meeting_chat_data(sample_index=0,assets_dir=None):return generate_data('meeting_chat',sample_index,assets_dir)
apply_meeting_chat_state=apply_state
