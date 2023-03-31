"""SHow the distribution of interactions in a Sessio.
"""

from src.sessions_util import SessionsUtils as su
from src.sessions_random import Sessions

def test_get_session_interactions():
    #breakpoint()
    sc = Sessions()
    interactions = su.get_session_interactions(session=sc)
    assert interactions is not None



def test_show_ascii_histogram():
    sc = Sessions()
    interactions = su.get_session_interactions(session=sc)
    assert interactions is not None
    x = su.show_ascii_histogram(interactions=interactions)
