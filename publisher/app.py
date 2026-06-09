import aio_pika
import asyncio
import json
import urllib.parse

from telegram import (
Bot,
InlineKeyboardButton,
InlineKeyboardMarkup
)

from publisher.formatter import (
format_product_message
)

from core.config.settings import settings
from core.telemetry.logger import logger

telegram_bot = Bot(
token=settings.TELEGRAM_TOKEN
)

async def process_message(
message: aio_pika.IncomingMessage
):

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

        message_text = format_product_message(
            body
        )

        print("\n===================")
        print("MENSAGEM FORMATADA")
        print(message_text)

        whatsapp_text = urllib.parse.quote(
            message_text
        )

        whatsapp_url = (
            f"https://wa.me/?text={whatsapp_text}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🟢 Compartilhar WhatsApp",
                    url=whatsapp_url
                )
            ]
        ])

        await telegram_bot.send_photo(
            chat_id=body["chat_id"],
            photo=body["image"],
            caption=message_text,
            parse_mode="HTML",
            reply_markup=keyboard
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
        routing_key="product.enriched"
    )

    await queue.consume(
        process_message
    )

    logger.info(
        "Publisher iniciado",
        extra={
            "service": "publisher"
        }
    )

    await asyncio.Future()


asyncio.run(main())
