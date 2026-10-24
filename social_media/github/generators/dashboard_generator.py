from .shared import generate_data,apply_state
DASHBOARD_STATES=('feed', 'repositories', 'following', 'empty', 'new_repository', 'notifications')
def generate_dashboard_data(sample_index=0,assets_dir=None):return generate_data('dashboard',sample_index,assets_dir)
def apply_dashboard_state(base,state):return apply_state(base,state)
