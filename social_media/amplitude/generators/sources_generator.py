from .shared import generate_data,apply_state
SOURCES_STATES=['connected', 'available', 'errors', 'setup', 'source_setup', 'source_menu']
def generate_sources_data(sample_index=0,assets_dir=None):return generate_data('sources',sample_index,assets_dir)
apply_sources_state=apply_state
