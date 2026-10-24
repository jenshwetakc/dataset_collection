from .shared import generate_data,apply_state
DASHBOARD_STATES=['overview', 'editing', 'compare', 'filtered', 'share_dashboard', 'date_panel']
def generate_dashboard_data(sample_index=0,assets_dir=None):return generate_data('dashboard',sample_index,assets_dir)
apply_dashboard_state=apply_state
