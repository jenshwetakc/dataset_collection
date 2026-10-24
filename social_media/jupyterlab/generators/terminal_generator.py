from .shared import generate_data,apply_state
TERMINAL_STATES=['shell', 'output', 'split', 'process_running', 'disconnected', 'shutdown_terminal']
def generate_terminal_data(sample_index=0,assets_dir=None):return generate_data('terminal',sample_index,assets_dir)
apply_terminal_state=apply_state
