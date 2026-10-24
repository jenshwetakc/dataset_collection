from .shared import generate_data,apply_state
QUIZ_STATES=('intro', 'question', 'answered', 'results', 'review_answers', 'exit_quiz')
def generate_quiz_data(sample_index=0,assets_dir=None):return generate_data('quiz',sample_index,assets_dir)
def apply_quiz_state(base,state):return apply_state(base,state)
