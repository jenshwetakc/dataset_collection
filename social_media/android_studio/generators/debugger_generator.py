from .shared import generate_data,apply_state
DEBUGGER_STATES=['attached', 'paused', 'variables', 'breakpoints', 'disconnected', 'evaluate_expression']
def generate_debugger_data(sample_index=0,assets_dir=None):return generate_data('debugger',sample_index,assets_dir)
apply_debugger_state=apply_state
