from .shared import generate_data,apply_state
FITNESS_PROGRAMS_STATES=['featured', 'strength', 'stretching', 'saved', 'program_detail', 'cookie_corner']
def generate_fitness_programs_data(sample_index=0,assets_dir=None):return generate_data('fitness_programs',sample_index,assets_dir)
apply_fitness_programs_state=apply_state
