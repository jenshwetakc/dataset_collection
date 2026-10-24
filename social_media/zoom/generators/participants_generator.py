from .shared import generate_data,apply_state
PARTICIPANTS_STATES=['all', 'waiting', 'raised_hands', 'searching', 'participant_menu', 'invite_dialog']
def generate_participants_data(sample_index=0,assets_dir=None):return generate_data('participants',sample_index,assets_dir)
apply_participants_state=apply_state
