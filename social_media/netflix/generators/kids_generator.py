from .shared import generate_data,apply_state
KIDS_STATES=('home', 'characters', 'movies', 'series', 'exit_kids', 'parental_controls')
def generate_kids_data(sample_index=0,assets_dir=None):return generate_data('kids',sample_index,assets_dir)
def apply_kids_state(base,state):return apply_state(base,state)
