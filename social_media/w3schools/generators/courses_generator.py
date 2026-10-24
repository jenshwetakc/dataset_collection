from .shared import generate_data,apply_state
COURSES_STATES=('catalog', 'course_detail', 'curriculum', 'enrolled', 'cart', 'advertisement')
def generate_courses_data(sample_index=0,assets_dir=None):return generate_data('courses',sample_index,assets_dir)
def apply_courses_state(base,state):return apply_state(base,state)
