from .shared import generate_data,apply_state
CONSOLE_STATES=['ready', 'history', 'running', 'error', 'kernel_disconnected', 'change_kernel']
def generate_console_data(sample_index=0,assets_dir=None):return generate_data('console',sample_index,assets_dir)
apply_console_state=apply_state
