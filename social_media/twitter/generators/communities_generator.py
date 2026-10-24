from .shared import generate_data,apply_state
COMMUNITIES_STATES=['discover', 'joined', 'popular', 'newest', 'create_community', 'community_filters']
def generate_communities_data(sample_index=0,assets_dir=None):return generate_data('communities',sample_index,assets_dir)
apply_communities_state=apply_state
