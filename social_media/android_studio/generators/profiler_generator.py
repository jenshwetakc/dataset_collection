from .shared import generate_data,apply_state
PROFILER_STATES=['overview', 'cpu', 'memory', 'network', 'recording', 'capture_options']
def generate_profiler_data(sample_index=0,assets_dir=None):return generate_data('profiler',sample_index,assets_dir)
apply_profiler_state=apply_state
