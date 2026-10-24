from .shared import generate_data,apply_state
EXPERIMENTS_STATES=['all', 'running', 'completed', 'drafts', 'new_experiment', 'experiment_menu']
def generate_experiments_data(sample_index=0,assets_dir=None):return generate_data('experiments',sample_index,assets_dir)
apply_experiments_state=apply_state
