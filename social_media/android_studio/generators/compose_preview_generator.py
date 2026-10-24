from .shared import generate_data,apply_state
COMPOSE_PREVIEW_STATES=['preview', 'multi_preview', 'interactive', 'render_error', 'refreshing', 'preview_config']
def generate_compose_preview_data(sample_index=0,assets_dir=None):return generate_data('compose_preview',sample_index,assets_dir)
apply_compose_preview_state=apply_state
