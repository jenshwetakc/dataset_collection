from .shared import generate_data,apply_state
FUNNEL_STATES=['conversion', 'over_time', 'time_to_convert', 'breakdown', 'step_panel', 'filter_panel']
def generate_funnel_data(sample_index=0,assets_dir=None):return generate_data('funnel',sample_index,assets_dir)
apply_funnel_state=apply_state
