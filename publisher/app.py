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
from core.telemetry.context import set_context

from core.telemetry.metrics import (
    PRODUCT_PUBLISHED_TOTAL,
    PROCESSING_TIME
)

telegram_bot = Bot(
    token=settings.TELEGRAM_TOKEN
)


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
                    service="publisher"
                )

                logger.info(
                    "Evento recebido para publicação"
                )

                message_text = (
                    format_product_message(
                        body
                    )
                )

                logger.info(
                    "Mensagem formatada",
                    extra={
                        "title": body.get(
                            "title"
                        ),
                        "message_size": len(
                            message_text
                        )
                    }
                )

                whatsapp_text = (
                    urllib.parse.quote(
                        message_text
                    )
                )

                whatsapp_url = (
                    f"https://wa.me/?text={whatsapp_text}"
                )

                logger.info(
                    "Link WhatsApp gerado"
                )

                keyboard = (
                    InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "🟢 Compartilhar WhatsApp",
                                url=whatsapp_url
                            )
                        ]
                    ])
                )

                logger.info(
                    "Enviando mensagem Telegram",
                    extra={
                        "chat_id": body.get(
                            "chat_id"
                        )
                    }
                )

                await telegram_bot.send_photo(
                    chat_id=body["chat_id"],
                    photo=body["image"],
                    caption=message_text,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )

                PRODUCT_PUBLISHED_TOTAL.inc()

                logger.info(
                    "Mensagem enviada com sucesso"
                )

        except Exception as e:

            logger.exception(
                f"Erro ao publicar mensagem: {str(e)}"
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
        "Publisher iniciado"
    )

    await asyncio.Future()


asyncio.run(main())