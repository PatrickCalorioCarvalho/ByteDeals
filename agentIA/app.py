import aio_pika
import asyncio
import json

from core.config.settings import settings

from core.telemetry.logger import logger
from core.telemetry.context import set_context

from core.telemetry.metrics import (
    PRODUCT_ENRICHED_TOTAL,
    PROCESSING_TIME
)

from core.rabbit.publisher import RabbitPublisher

from core.events.product_enriched import (
    ProductEnrichedEvent
)

from agentIA.prompt_builder import (
    build_prompt
)

from agentIA.ollama_client import (
    generate_text
)

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
                    service="agentia"
                )

                logger.info(
                    "Evento recebido para enriquecimento"
                )

                prompt = build_prompt(
                    body
                )

                logger.info(
                    "Prompt gerado",
                    extra={
                        "title": body.get(
                            "title"
                        )
                    }
                )

                ai_text = await generate_text(
                    prompt
                )

                logger.info(
                    "Resposta IA recebida",
                    extra={
                        "response_size": len(
                            ai_text
                        )
                    }
                )

                enriched_event = (
                    ProductEnrichedEvent(
                        correlation_id=body.get(
                            "correlation_id"
                        ),
                        trace_id=body.get(
                            "trace_id"
                        ),
                        source_service="agentia",
                        chat_id=body.get(
                            "chat_id"
                        ),
                        title=body.get(
                            "title"
                        ),
                        image=body.get(
                            "image"
                        ),
                        old_price=body.get(
                            "old_price"
                        ),
                        new_price=body.get(
                            "new_price"
                        ),
                        discount=body.get(
                            "discount"
                        ),
                        economy=body.get(
                            "economy"
                        ),
                        link=body.get(
                            "link"
                        ),
                        ai_text=ai_text.strip()
                    )
                )

                await publisher.publish(
                    "product.enriched",
                    enriched_event
                )

                PRODUCT_ENRICHED_TOTAL.inc()

                logger.info(
                    "Evento product.enriched publicado"
                )

        except Exception as e:

            logger.exception(
                f"Erro no AgentIA: {str(e)}"
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
        "agentia.queue",
        durable=True
    )

    await queue.bind(
        exchange,
        routing_key="product.extracted"
    )

    await queue.consume(
        process_message
    )

    logger.info(
        "AgentIA iniciado"
    )

    await asyncio.Future()


asyncio.run(main())