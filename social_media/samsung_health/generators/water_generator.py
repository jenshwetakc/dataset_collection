from .shared import generate_data,apply_state
WATER_STATES=['today', 'week', 'goal_reached', 'empty', 'water_goal', 'cup_size']
def generate_water_data(sample_index=0,assets_dir=None):return generate_data('water',sample_index,assets_dir)
apply_water_state=apply_state
