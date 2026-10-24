from .shared import generate_data,apply_state
REQUIREMENTS_STATES=['draft', 'generated', 'editing', 'validated', 'needs_revision', 'delete_spec']
def generate_requirements_data(sample_index=0,assets_dir=None):return generate_data('requirements',sample_index,assets_dir)
apply_requirements_state=apply_state
