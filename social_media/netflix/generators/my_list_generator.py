from .shared import generate_data,apply_state
MY_LIST_STATES=('all', 'movies', 'series', 'empty', 'sort', 'remove_title')
def generate_my_list_data(sample_index=0,assets_dir=None):return generate_data('my_list',sample_index,assets_dir)
def apply_my_list_state(base,state):return apply_state(base,state)
