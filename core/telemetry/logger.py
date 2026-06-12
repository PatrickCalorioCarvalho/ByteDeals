import json
import logging
import sys

from core.telemetry.context import (
    get_context
)


class JsonFormatter(
    logging.Formatter
):

    def format(
        self,
        record
    ):

        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }

        payload.update(
            get_context()
        )

        return json.dumps(
            payload,
            ensure_ascii=False
        )


logger = logging.getLogger(
    "bytedeals"
)

logger.setLevel(
    logging.INFO
)

handler = logging.StreamHandler(
    sys.stdout
)

handler.setFormatter(
    JsonFormatter()
)

logger.handlers.clear()

logger.addHandler(
    handler
)