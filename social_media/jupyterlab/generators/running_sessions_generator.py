from .shared import generate_data,apply_state
RUNNING_SESSIONS_STATES=['active', 'expanded', 'idle', 'filtered', 'shutdown_kernel', 'shutdown_all']
def generate_running_sessions_data(sample_index=0,assets_dir=None):return generate_data('running_sessions',sample_index,assets_dir)
apply_running_sessions_state=apply_state
