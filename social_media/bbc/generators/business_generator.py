from .shared import generate_data,apply_state
BUSINESS_STATES=['headlines', 'markets', 'economy', 'technology', 'market_filter', 'newsletter_dialog']
def generate_business_data(sample_index=0,assets_dir=None):return generate_data('business',sample_index,assets_dir)
apply_business_state=apply_state
