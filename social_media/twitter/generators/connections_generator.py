from .shared import generate_data,apply_state
CONNECTIONS_STATES=['followers', 'following', 'verified_followers', 'suggested', 'unfollow_dialog', 'block_dialog']
def generate_connections_data(sample_index=0,assets_dir=None):return generate_data('connections',sample_index,assets_dir)
apply_connections_state=apply_state
