import aio_pika
import asyncio
import json
from prometheus_client import start_http_server
from core.config.settings import settings
from core.telemetry.logger import logger
from extractor.parser import extract_product
from extractor.downloader import fetch_html
from core.events.product_extracted import (
ProductExtractedEvent
)
from core.rabbit.publisher import RabbitPublisher
from core.telemetry.metrics import (
    MESSAGES_TOTAL,
    PROCESSING_TIME
)

start_http_server(8002)
publisher = RabbitPublisher()

async def process_message(
message: aio_pika.IncomingMessage
):
    async with message.process():
        try:
            with PROCESSING_TIME.time():

                body = json.loads(message.body)

                MESSAGES_TOTAL.inc()

                logger.info(
                    "Produto recebido",
                    extra={
                        "service": "extractor",
                        "correlation_id": body.get("correlation_id")
                    }
                )

                print(body)

                url = body.get("url")

                html = await fetch_html(url)

                product = extract_product(html)

                logger.info(
                    "Produto extraído",
                    extra={
                        "service": "extractor",
                        "correlation_id": body.get("correlation_id")
                    }
                )
                extracted_event = ProductExtractedEvent(
                    correlation_id=body.get("correlation_id"),
                    chat_id=body.get("chat_id"),
                    title=product.get("title"),
                    image=product.get("image"),
                    old_price=product.get("old_price"),
                    new_price=product.get("new_price"),
                    discount=product.get("discount"),
                    economy=product.get("economy"),
                    link=url
                )
                await publisher.publish(
                    "product.extracted",
                    extracted_event
                )

                logger.info(
                    "Processamento concluído com sucesso",
                    extra={
                        "service": "extractor",
                        "correlation_id": body.get("correlation_id")
                    }
                )
        except Exception as e:
            logger.info(
                f"Erro ao processar mensagem: {str(e)}",
                extra={
                    "service": "extractor"
                }
            )
            print(f"ERROR: {str(e)}")
            raise

async def main():
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASS
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

    await queue.consume(process_message)

    logger.info(
        "Extractor iniciado",
        extra={
            "service": "extractor"
        }
    )

    await asyncio.Future()

asyncio.run(main())
