from .shared import generate_data,apply_state
ROUTE_STATES=['map', 'elevation', 'laps', 'offline', 'route_options', 'location_permission']
def generate_route_data(sample_index=0,assets_dir=None):return generate_data('route',sample_index,assets_dir)
apply_route_state=apply_state
