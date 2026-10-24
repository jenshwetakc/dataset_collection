from .shared import generate_data,apply_state
NEW_POPULAR_STATES=('coming_soon', 'everyone_watching', 'top_ten', 'reminder_set', 'reminder_options', 'preview')
def generate_new_popular_data(sample_index=0,assets_dir=None):return generate_data('new_popular',sample_index,assets_dir)
def apply_new_popular_state(base,state):return apply_state(base,state)
