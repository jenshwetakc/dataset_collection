from .shared import generate_data,apply_state
CONTACTS_STATES=['all', 'starred', 'external', 'requests', 'add_contact_dialog', 'contact_menu']
def generate_contacts_data(sample_index=0,assets_dir=None):return generate_data('contacts',sample_index,assets_dir)
apply_contacts_state=apply_state
