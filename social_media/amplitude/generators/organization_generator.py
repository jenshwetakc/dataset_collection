from .shared import generate_data,apply_state
ORGANIZATION_STATES=['members', 'teams', 'projects', 'billing', 'invite_members', 'role_panel']
def generate_organization_data(sample_index=0,assets_dir=None):return generate_data('organization',sample_index,assets_dir)
apply_organization_state=apply_state
