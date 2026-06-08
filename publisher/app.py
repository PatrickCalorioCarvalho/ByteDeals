import aio_pika
import asyncio
import json

from telegram import Bot

from core.config.settings import settings
from core.telemetry.logger import logger

telegram_bot = Bot(token=settings.TELEGRAM_TOKEN)

async def process_message(message: aio_pika.IncomingMessage):

    async with message.process():

        body = json.loads(message.body)

        logger.info(
            "Enviando mensagem Telegram",
            extra={
                "service": "publisher",
                "correlation_id": body.get(
                    "correlation_id"
                )
            }
        )

        await telegram_bot.send_photo(
            chat_id=body["chat_id"],
            photo=body["image"],
            caption=body["message"]
        )

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
        "publisher.queue",
        durable=True
    )

    await queue.bind(
        exchange,
        routing_key="product.formatted"
    )

    await queue.consume(process_message)

    logger.info(
        "Publisher iniciado",
        extra={
            "service": "publisher"
        }
    )

    await asyncio.Future()

asyncio.run(main())
