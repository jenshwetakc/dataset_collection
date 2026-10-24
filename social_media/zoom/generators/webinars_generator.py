from .shared import generate_data,apply_state
WEBINARS_STATES=['upcoming', 'past', 'drafts', 'registrants', 'new_webinar_dialog', 'webinar_menu']
def generate_webinars_data(sample_index=0,assets_dir=None):return generate_data('webinars',sample_index,assets_dir)
apply_webinars_state=apply_state
