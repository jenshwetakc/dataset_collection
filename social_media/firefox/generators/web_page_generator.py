from .shared import generate_data,apply_state
WEB_PAGE_STATES=['loaded', 'reader_mode', 'cookie_banner', 'cookie_side', 'permission_panel', 'find_in_page']
def generate_web_page_data(sample_index=0,assets_dir=None):return generate_data('web_page',sample_index,assets_dir)
apply_web_page_state=apply_state
