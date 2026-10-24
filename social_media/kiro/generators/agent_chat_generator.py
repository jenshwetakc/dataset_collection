from .shared import generate_data,apply_state
AGENT_CHAT_STATES=['empty', 'conversation', 'generating', 'context_attached', 'permission_request', 'clear_chat']
def generate_agent_chat_data(sample_index=0,assets_dir=None):return generate_data('agent_chat',sample_index,assets_dir)
apply_agent_chat_state=apply_state
