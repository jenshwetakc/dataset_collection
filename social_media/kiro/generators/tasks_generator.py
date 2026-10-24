from .shared import generate_data,apply_state
TASKS_STATES=['planned', 'running', 'completed', 'failed', 'optional_tasks', 'stop_task']
def generate_tasks_data(sample_index=0,assets_dir=None):return generate_data('tasks',sample_index,assets_dir)
apply_tasks_state=apply_state
