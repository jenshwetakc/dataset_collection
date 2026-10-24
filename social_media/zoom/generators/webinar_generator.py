from .shared import generate_data,apply_state
WEBINAR_STATES=['attendee', 'presenter', 'qa', 'polls', 'question_dialog', 'leave_dialog']
def generate_webinar_data(sample_index=0,assets_dir=None):return generate_data('webinar',sample_index,assets_dir)
apply_webinar_state=apply_state
