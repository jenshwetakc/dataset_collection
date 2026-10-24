from .shared import generate_data,apply_state
CHANNEL_STATES=['messages', 'files', 'pinned', 'typing', 'channel_info', 'add_members_dialog']
def generate_channel_data(sample_index=0,assets_dir=None):return generate_data('channel',sample_index,assets_dir)
apply_channel_state=apply_state
