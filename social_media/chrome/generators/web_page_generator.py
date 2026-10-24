from .shared import generate_data,apply_state
WEB_PAGE_STATES=('loaded', 'loading', 'offline', 'find', 'browser_menu', 'save_bookmark')
def generate_web_page_data(sample_index=0,assets_dir=None):return generate_data('web_page',sample_index,assets_dir)
def apply_web_page_state(base,state):return apply_state(base,state)
