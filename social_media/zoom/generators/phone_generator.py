from .shared import generate_data,apply_state
PHONE_STATES=['dialpad', 'history', 'voicemail', 'calling', 'call_menu', 'call_dialog']
def generate_phone_data(sample_index=0,assets_dir=None):return generate_data('phone',sample_index,assets_dir)
apply_phone_state=apply_state
