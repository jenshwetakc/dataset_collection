from .shared import generate_data,apply_state
WAITING_ROOM_STATES=['waiting', 'admitted', 'host_message', 'audio_test', 'leave_dialog', 'device_panel']
def generate_waiting_room_data(sample_index=0,assets_dir=None):return generate_data('waiting_room',sample_index,assets_dir)
apply_waiting_room_state=apply_state
