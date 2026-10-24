from .shared import generate_data,apply_state
CERTIFICATES_STATES=('overview', 'exam_instructions', 'practice_exam', 'earned', 'verify_certificate', 'exam_confirmation')
def generate_certificates_data(sample_index=0,assets_dir=None):return generate_data('certificates',sample_index,assets_dir)
def apply_certificates_state(base,state):return apply_state(base,state)
