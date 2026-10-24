from .shared import generate_data,apply_state
GOTO_ANYTHING_STATES=['files', 'symbols', 'line', 'no_results', 'preview', 'open_recent']
def generate_goto_anything_data(sample_index=0,assets_dir=None):return generate_data('goto_anything',sample_index,assets_dir)
apply_goto_anything_state=apply_state
