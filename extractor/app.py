import aio_pika
import asyncio
import json

from prometheus_client import start_http_server

from core.config.settings import settings

from core.telemetry.logger import logger
from core.telemetry.context import set_context

from core.telemetry.metrics import (
    PRODUCT_RECEIVED_TOTAL,
    PRODUCT_EXTRACTED_TOTAL,
    PROCESSING_TIME
)

from extractor.downloader import fetch_html
from extractor.parser import extract_product

from core.rabbit.publisher import RabbitPublisher

from core.events.product_extracted import (
    ProductExtractedEvent
)

start_http_server(8002)

publisher = RabbitPublisher()


async def process_message(
    message: aio_pika.IncomingMessage
):

    async with message.process():

        try:

            with PROCESSING_TIME.time():

                body = json.loads(
                    message.body
                )

                set_context(
                    correlation_id=body.get(
                        "correlation_id"
                    ),
                    trace_id=body.get(
                        "trace_id"
                    ),
                    event_id=body.get(
                        "event_id"
                    ),
                    service="extractor"
                )

                PRODUCT_RECEIVED_TOTAL.inc()

                logger.info(
                    "Evento recebido"
                )

                url = body.get("url")

                logger.info(
                    "Baixando HTML",
                    extra={
                        "url": url
                    }
                )

                html = await fetch_html(
                    url
                )

                logger.info(
                    "HTML carregado"
                )

                product = extract_product(
                    html
                )

                PRODUCT_EXTRACTED_TOTAL.inc()

                logger.info(
                    "Produto extraído",
                    extra={
                        "title": product.get(
                            "title"
                        ),
                        "old_price": product.get(
                            "old_price"
                        ),
                        "new_price": product.get(
                            "new_price"
                        )
                    }
                )

                extracted_event = (
                    ProductExtractedEvent(
                        correlation_id=body.get(
                            "correlation_id"
                        ),
                        trace_id=body.get(
                            "trace_id"
                        ),
                        source_service="extractor",
                        chat_id=body.get(
                            "chat_id"
                        ),
                        title=product.get(
                            "title"
                        ),
                        image=product.get(
                            "image"
                        ),
                        old_price=product.get(
                            "old_price"
                        ),
                        new_price=product.get(
                            "new_price"
                        ),
                        discount=product.get(
                            "discount"
                        ),
                        economy=product.get(
                            "economy"
                        ),
                        link=url
                    )
                )

                await publisher.publish(
                    "product.extracted",
                    extracted_event
                )

                logger.info(
                    "Evento product.extracted publicado"
                )

        except Exception as e:

            logger.exception(
                f"Erro processando mensagem: {str(e)}"
            )

            raise


async def main():

    connection = (
        await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASS
        )
    )

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "bytedeals.events",
        aio_pika.ExchangeType.TOPIC,
        durable=True
    )

    queue = await channel.declare_queue(
        "extractor.queue",
        durable=True
    )

    await queue.bind(
        exchange,
        routing_key="product.received"
    )

    await queue.consume(
        process_message
    )

    logger.info(
        "Extractor iniciado"
    )

    await asyncio.Future()


asyncio.run(main())