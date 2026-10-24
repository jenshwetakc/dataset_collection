from .shared import generate_data,apply_state
AUCTIONS_OFFERS_STATES=('bidding', 'outbid', 'winning', 'offer_pending', 'place_bid', 'make_offer')
def generate_auctions_offers_data(sample_index=0,assets_dir=None):
    return generate_data('auctions_offers',sample_index,assets_dir)
def apply_auctions_offers_state(base_data,state):
    return apply_state(base_data,state)
