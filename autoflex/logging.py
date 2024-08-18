import logging
from sphinx.application import Sphinx

# Define the logger at the module level
logger = logging.getLogger(__name__)

def setup_logging(app: Sphinx):
    """Set up logging based on Sphinx config."""
    enable_logging = app.config.autoflex_logging
    logging_level = app.config.autoflex_logging_level

    if enable_logging:
        # Configure the logger if logging is enabled
        logging.basicConfig(level=getattr(logging, logging_level.upper(), 'DEBUG'))
        logger.debug("Logging is enabled for this extension")
    else:
        logger.disabled = True
