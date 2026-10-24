from .shared import generate_data,apply_state
NEWS_STATES=['world', 'uk', 'politics', 'most_read', 'region_menu', 'breaking_alert']
def generate_news_data(sample_index=0,assets_dir=None):return generate_data('news',sample_index,assets_dir)
apply_news_state=apply_state
