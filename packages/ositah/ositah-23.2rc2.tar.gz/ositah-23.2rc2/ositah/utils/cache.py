# Helper functions to manage the data cache

from .exceptions import SessionDataMissing
from .utils import GlobalParams, no_session_id_jumbotron


def clear_cached_data():
    """
    Clear the data cached by the previous requests

    :return: None
    """

    global_params = GlobalParams()
    try:
        session_data = global_params.get_session_data()
        session_data.reset_caches()
    except SessionDataMissing:
        return no_session_id_jumbotron()
