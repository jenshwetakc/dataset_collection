from .shared import generate_data,apply_state
TRAVEL_STATES=['destinations', 'guides', 'food', 'sustainable', 'destination_picker', 'cookie_corner']
def generate_travel_data(sample_index=0,assets_dir=None):return generate_data('travel',sample_index,assets_dir)
apply_travel_state=apply_state
