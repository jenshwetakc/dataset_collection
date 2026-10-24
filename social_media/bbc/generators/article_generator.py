from .shared import generate_data,apply_state
ARTICLE_STATES=['reading', 'share_menu', 'save_dialog', 'cookie_preferences', 'text_settings', 'advertisement']
def generate_article_data(sample_index=0,assets_dir=None):return generate_data('article',sample_index,assets_dir)
apply_article_state=apply_state
