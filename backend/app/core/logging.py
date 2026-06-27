import logging
import sys
from typing import Any, Dict

def setup_logging():
    """
    Configures a standard Python logger.
    For production, this would be enhanced with python-json-logger 
    for structured Datadog/ELK ingestion, but for now we keep it standard 
    and clean to meet requirements without heavy external dependencies.
    """
    logger = logging.getLogger("vedic_ai")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if setup_logging is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

log = setup_logging()
