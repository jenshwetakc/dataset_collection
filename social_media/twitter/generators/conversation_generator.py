from .shared import generate_data,apply_state
CONVERSATION_STATES=['chat', 'typing', 'attachment', 'message_menu', 'delete_dialog', 'conversation_info']
def generate_conversation_data(sample_index=0,assets_dir=None):return generate_data('conversation',sample_index,assets_dir)
apply_conversation_state=apply_state
