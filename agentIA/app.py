import aio_pika
import asyncio
import json
from core.telemetry.logger import logger
from core.config.settings import settings
from agentIA.prompt_builder import build_prompt
from agentIA.ollama_client import generate_text
from core.rabbit.publisher import RabbitPublisher
from core.events.product_enriched import (
    ProductEnrichedEvent
)

publisher = RabbitPublisher()

async def process_message(
message: aio_pika.IncomingMessage
):

    async with message.process():

        body = json.loads(message.body)
        print("\n===================")
        print("MENSAGEM RECEBIDA")
        print(body)

        prompt = build_prompt(body)
        print("\n===================")  
        print("PROMPT GERADO")
        print(prompt)

        ai_text = await generate_text(prompt)

        enriched_event = ProductEnrichedEvent(
            correlation_id=body.get("correlation_id"),
            chat_id=body.get("chat_id"),
            title=body.get("title"),
            image=body.get("image"),
            old_price=body.get("old_price"),
            new_price=body.get("new_price"),
            discount=body.get("discount"),
            economy=body.get("economy"),
            link=body.get("link"),
            ai_text=ai_text.strip()
        )
        await publisher.publish(
            "product.enriched",
            enriched_event
        )
        logger.info(
            "Mensagem IA gerada",
            extra={
                "service": "agentia",
                "correlation_id": body.get(
                    "correlation_id"
                )
            }
        )

        print("\n===================")
        print(ai_text)
        print("===================\n")


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
        "agentia.queue",
        durable=True
    )

    await queue.bind(
        exchange,
        routing_key="product.extracted"
    )

    await queue.consume(process_message)

    logger.info(
        "AgentIA iniciado",
        extra={
            "service": "agentia"
        }
    )

    await asyncio.Future()

asyncio.run(main())
