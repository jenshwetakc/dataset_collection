from .shared import generate_data,apply_state
DOWNLOADS_STATES=('available', 'downloading', 'expired', 'empty', 'smart_downloads', 'delete_download')
def generate_downloads_data(sample_index=0,assets_dir=None):return generate_data('downloads',sample_index,assets_dir)
def apply_downloads_state(base,state):return apply_state(base,state)
