from .shared import generate_data,apply_state
EXPERIMENT_DETAIL_STATES=['results', 'setup', 'metrics', 'diagnostics', 'launch_dialog', 'variant_panel']
def generate_experiment_detail_data(sample_index=0,assets_dir=None):return generate_data('experiment_detail',sample_index,assets_dir)
apply_experiment_detail_state=apply_state
