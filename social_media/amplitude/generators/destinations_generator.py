from .shared import generate_data,apply_state
DESTINATIONS_STATES=['connected', 'available', 'sync_history', 'failed', 'destination_setup', 'destination_menu']
def generate_destinations_data(sample_index=0,assets_dir=None):return generate_data('destinations',sample_index,assets_dir)
apply_destinations_state=apply_state
