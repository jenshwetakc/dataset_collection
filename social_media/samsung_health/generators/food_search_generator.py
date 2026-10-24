from .shared import generate_data,apply_state
FOOD_SEARCH_STATES=['results', 'recent', 'favorites', 'typing', 'portion_dialog', 'create_food']
def generate_food_search_data(sample_index=0,assets_dir=None):return generate_data('food_search',sample_index,assets_dir)
apply_food_search_state=apply_state
