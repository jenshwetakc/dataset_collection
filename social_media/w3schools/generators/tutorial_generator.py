from .shared import generate_data,apply_state
TUTORIAL_STATES=('introduction', 'headings', 'tables', 'chapter_complete', 'mobile_contents', 'advertisement')
def generate_tutorial_data(sample_index=0,assets_dir=None):return generate_data('tutorial',sample_index,assets_dir)
def apply_tutorial_state(base,state):return apply_state(base,state)
