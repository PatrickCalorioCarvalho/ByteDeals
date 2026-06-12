import aio_pika

from core.config.settings import settings
from core.telemetry.logger import logger
from core.rabbit.observer import EventObserver

from core.telemetry.metrics import (
RABBIT_MESSAGES_PUBLISHED,
EVENTS_TOTAL,
ERRORS_TOTAL
)

class RabbitPublisher:

    async def publish(
        self,
        routing_key: str,
        event
    ):

        connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASS
        )

        try:

            channel = await connection.channel()

            exchange = await channel.declare_exchange(
                "bytedeals.events",
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )

            await exchange.publish(
                aio_pika.Message(
                    body=event.model_dump_json().encode()
                ),
                routing_key=routing_key
            )

            RABBIT_MESSAGES_PUBLISHED.inc()
            EVENTS_TOTAL.inc()

            EventObserver.event_published(
                routing_key=routing_key,
                event=event
            )

            logger.info(
                "Evento publicado no RabbitMQ",
                extra={
                    "routing_key": routing_key,
                    "event_id": getattr(event, "event_id", None),
                    "correlation_id": getattr(event, "correlation_id", None),
                    "trace_id": getattr(event, "trace_id", None),
                    "service": "rabbit"
                }
            )

        except Exception:

            ERRORS_TOTAL.inc()

            logger.exception(
                "Falha ao publicar evento",
                extra={
                    "routing_key": routing_key,
                    "event_id": getattr(event, "event_id", None),
                    "correlation_id": getattr(event, "correlation_id", None),
                    "service": "rabbit"
                }
            )

            raise

        finally:

            await connection.close()
