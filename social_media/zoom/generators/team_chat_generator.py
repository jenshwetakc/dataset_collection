from .shared import generate_data,apply_state
TEAM_CHAT_STATES=['all', 'unread', 'mentions', 'empty', 'new_chat_dialog', 'notification_panel']
def generate_team_chat_data(sample_index=0,assets_dir=None):return generate_data('team_chat',sample_index,assets_dir)
apply_team_chat_state=apply_state
