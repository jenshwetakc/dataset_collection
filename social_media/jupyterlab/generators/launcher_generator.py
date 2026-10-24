from .shared import generate_data,apply_state
LAUNCHER_STATES=['default', 'recent', 'empty', 'command_palette', 'new_folder', 'choose_kernel']
def generate_launcher_data(sample_index=0,assets_dir=None):return generate_data('launcher',sample_index,assets_dir)
apply_launcher_state=apply_state
