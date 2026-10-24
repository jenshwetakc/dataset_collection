from .shared import generate_data,apply_state
PROPERTIES_STATES=['event_properties', 'user_properties', 'group_properties', 'searching', 'property_detail', 'property_menu']
def generate_properties_data(sample_index=0,assets_dir=None):return generate_data('properties',sample_index,assets_dir)
apply_properties_state=apply_state
