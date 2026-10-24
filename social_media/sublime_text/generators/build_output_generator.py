from .shared import generate_data,apply_state
BUILD_OUTPUT_STATES=['success', 'running', 'error', 'test_results', 'configuration', 'cancel_build']
def generate_build_output_data(sample_index=0,assets_dir=None):return generate_data('build_output',sample_index,assets_dir)
apply_build_output_state=apply_state
