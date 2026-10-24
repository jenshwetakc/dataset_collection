from .shared import generate_data,apply_state
FIND_REPLACE_STATES=['find', 'replace', 'regex', 'no_matches', 'find_all', 'replace_confirm']
def generate_find_replace_data(sample_index=0,assets_dir=None):return generate_data('find_replace',sample_index,assets_dir)
apply_find_replace_state=apply_state
