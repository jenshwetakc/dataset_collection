from .shared import generate_data,apply_state
MCP_STATES=['servers', 'connected', 'disconnected', 'tools', 'configuration', 'add_server']
def generate_mcp_data(sample_index=0,assets_dir=None):return generate_data('mcp',sample_index,assets_dir)
apply_mcp_state=apply_state
