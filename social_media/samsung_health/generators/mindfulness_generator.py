from .shared import generate_data,apply_state
MINDFULNESS_STATES=['discover', 'breathing', 'meditation', 'favorites', 'session_player', 'mindfulness_reminder']
def generate_mindfulness_data(sample_index=0,assets_dir=None):return generate_data('mindfulness',sample_index,assets_dir)
apply_mindfulness_state=apply_state
