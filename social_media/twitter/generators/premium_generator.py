from .shared import generate_data,apply_state
PREMIUM_STATES=['overview', 'basic', 'premium', 'premium_plus', 'plan_dialog', 'billing_panel']
def generate_premium_data(sample_index=0,assets_dir=None):return generate_data('premium',sample_index,assets_dir)
apply_premium_state=apply_state
