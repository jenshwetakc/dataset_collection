from .shared import generate_data,apply_state
EVENT_SEGMENTATION_STATES=['line', 'bar', 'table', 'compare', 'event_picker', 'save_chart']
def generate_event_segmentation_data(sample_index=0,assets_dir=None):return generate_data('event_segmentation',sample_index,assets_dir)
apply_event_segmentation_state=apply_state
