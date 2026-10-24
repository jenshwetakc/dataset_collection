from .shared import generate_data,apply_state
PRINT_PREVIEW_STATES=('portrait', 'landscape', 'custom_pages', 'color', 'destination', 'printing')
def generate_print_preview_data(sample_index=0,assets_dir=None):return generate_data('print_preview',sample_index,assets_dir)
def apply_print_preview_state(base,state):return apply_state(base,state)
