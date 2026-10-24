from .shared import generate_data,apply_state
TOGETHER_STATES=['overview', 'friends', 'leaderboard', 'invites', 'invite_friend', 'challenge_menu']
def generate_together_data(sample_index=0,assets_dir=None):return generate_data('together',sample_index,assets_dir)
apply_together_state=apply_state
