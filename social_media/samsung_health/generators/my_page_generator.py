from .shared import generate_data,apply_state
MY_PAGE_STATES=['overview', 'achievements', 'personal_bests', 'editing', 'edit_profile', 'status_panel']
def generate_my_page_data(sample_index=0,assets_dir=None):return generate_data('my_page',sample_index,assets_dir)
apply_my_page_state=apply_state
