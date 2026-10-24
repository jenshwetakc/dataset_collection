from .shared import generate_data,apply_state
REWARDS_STATES=['overview', 'enabled', 'disabled', 'statement', 'rewards_panel', 'ad_notification']
def generate_rewards_data(sample_index=0,assets_dir=None):return generate_data('rewards',sample_index,assets_dir)
apply_rewards_state=apply_state
