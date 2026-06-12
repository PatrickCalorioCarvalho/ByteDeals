from core.telemetry.logger import logger

class EventObserver:

    @staticmethod
    def event_published(
        routing_key: str,
        event
    ):

        logger.info(
            "Evento publicado",
            extra={
                "routing_key": routing_key,
                "event_id": event.event_id,
                "correlation_id": event.correlation_id,
                "trace_id": event.trace_id,
                "source_service": event.source_service
            }
        )

    @staticmethod
    def event_received(
        routing_key: str,
        payload: dict
    ):

        logger.info(
            "Evento recebido",
            extra={
                "routing_key": routing_key,
                "event_id": payload.get("event_id"),
                "correlation_id": payload.get("correlation_id"),
                "trace_id": payload.get("trace_id"),
                "source_service": payload.get("source_service")
            }
        )