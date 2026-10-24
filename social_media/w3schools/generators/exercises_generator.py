from .shared import generate_data,apply_state
EXERCISES_STATES=('catalog', 'question', 'correct', 'incorrect', 'show_answer', 'reset_progress')
def generate_exercises_data(sample_index=0,assets_dir=None):return generate_data('exercises',sample_index,assets_dir)
def apply_exercises_state(base,state):return apply_state(base,state)
