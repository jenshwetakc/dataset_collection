from .shared import generate_data,apply_state
BUILD_STATES=['success', 'running', 'failed', 'tests', 'sync_required', 'build_options']
def generate_build_data(sample_index=0,assets_dir=None):return generate_data('build',sample_index,assets_dir)
apply_build_state=apply_state
