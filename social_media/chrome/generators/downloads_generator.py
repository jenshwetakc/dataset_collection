from .shared import generate_data,apply_state
DOWNLOADS_STATES=('completed', 'downloading', 'paused', 'failed', 'blocked', 'remove_download')
def generate_downloads_data(sample_index=0,assets_dir=None):return generate_data('downloads',sample_index,assets_dir)
def apply_downloads_state(base,state):return apply_state(base,state)
