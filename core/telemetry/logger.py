import logging
import json
import sys

class JsonFormatter(logging.Formatter):

    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service", "unknown"),
            "correlation_id": getattr(record, "correlation_id", None)
        }
        
        message = record.getMessage()
        service = getattr(record, "service", "unknown")
        correlation_id = getattr(record, "correlation_id", None)
        
        return f"{record.levelname} {message} | service={service} correlation_id={correlation_id}"

logger = logging.getLogger("bytedeals")
logger.propagate = False
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
