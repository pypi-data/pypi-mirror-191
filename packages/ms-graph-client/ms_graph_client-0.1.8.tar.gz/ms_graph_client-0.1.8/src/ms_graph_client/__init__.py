import logging


from ms_graph_client.services.graph_api import GraphAPI  # noqa: F401
from ms_graph_client.services_cache.graph_api import GraphAPI as GraphCacheAPI  # noqa: F401
from ms_graph_client.graph_api_config import GraphAPIConfig  # noqa: F401
from ms_graph_client.services.generator import Generator  # noqa: F401

# Package Logger
# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["GraphAPIConfig", "GraphAPI", "GraphCacheAPI", "Generator"]
