from .shared import generate_data,apply_state
PRIVACY_SAFETY_STATES=('privacy', 'comments', 'messages', 'blocked_accounts', 'report_problem', 'delete_account')
def generate_privacy_safety_data(sample_index=0,assets_dir=None):
    return generate_data('privacy_safety',sample_index,assets_dir)
def apply_privacy_safety_state(base_data,state):
    return apply_state(base_data,state)
