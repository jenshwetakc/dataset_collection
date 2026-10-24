from .shared import generate_data,apply_state
DASHBOARDS_STATES=['all', 'owned', 'shared', 'empty', 'new_dashboard', 'dashboard_menu']
def generate_dashboards_data(sample_index=0,assets_dir=None):return generate_data('dashboards',sample_index,assets_dir)
apply_dashboards_state=apply_state
