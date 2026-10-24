from .shared import generate_data,apply_state
CHALLENGE_STATES=['overview', 'ranking', 'milestones', 'completed', 'join_challenge', 'leave_challenge']
def generate_challenge_data(sample_index=0,assets_dir=None):return generate_data('challenge',sample_index,assets_dir)
apply_challenge_state=apply_state
