from .shared import generate_data,apply_state
CULTURE_STATES=['features', 'film', 'music', 'books', 'gallery', 'newsletter_dialog']
def generate_culture_data(sample_index=0,assets_dir=None):return generate_data('culture',sample_index,assets_dir)
apply_culture_state=apply_state
