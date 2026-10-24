from .shared import generate_data,apply_state
COMMAND_PALETTE_STATES=['commands', 'filtered', 'no_results', 'build_choices', 'syntax_choices', 'theme_choices']
def generate_command_palette_data(sample_index=0,assets_dir=None):return generate_data('command_palette',sample_index,assets_dir)
apply_command_palette_state=apply_state
