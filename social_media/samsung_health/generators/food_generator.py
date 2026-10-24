from .shared import generate_data,apply_state
FOOD_STATES=['today', 'week', 'nutrients', 'empty', 'meal_picker', 'food_goal']
def generate_food_data(sample_index=0,assets_dir=None):return generate_data('food',sample_index,assets_dir)
apply_food_state=apply_state
