from .shared import generate_data,apply_state
COMPOSE_STATES=['text', 'media', 'poll', 'scheduled', 'audience_panel', 'discard_dialog']
def generate_compose_data(sample_index=0,assets_dir=None):return generate_data('compose',sample_index,assets_dir)
apply_compose_state=apply_state
