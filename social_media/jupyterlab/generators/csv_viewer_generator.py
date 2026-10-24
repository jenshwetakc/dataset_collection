from .shared import generate_data,apply_state
CSV_VIEWER_STATES=['data', 'delimiter', 'missing_values', 'scrolled', 'empty', 'options']
def generate_csv_viewer_data(sample_index=0,assets_dir=None):return generate_data('csv_viewer',sample_index,assets_dir)
apply_csv_viewer_state=apply_state
