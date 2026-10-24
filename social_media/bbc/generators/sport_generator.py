from .shared import generate_data,apply_state
SPORT_STATES=['headlines', 'scores', 'fixtures', 'results', 'team_picker', 'follow_dialog']
def generate_sport_data(sample_index=0,assets_dir=None):return generate_data('sport',sample_index,assets_dir)
apply_sport_state=apply_state
