from .shared import generate_data,apply_state
JOURNEYS_STATES=['pathfinder', 'journey_map', 'before', 'after', 'path_panel', 'export_dialog']
def generate_journeys_data(sample_index=0,assets_dir=None):return generate_data('journeys',sample_index,assets_dir)
apply_journeys_state=apply_state
