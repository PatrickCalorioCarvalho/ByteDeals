from telegram import Update
from telegram.ext import (
ApplicationBuilder,
MessageHandler,
ContextTypes,
filters
)

from core.rabbit.publisher import RabbitPublisher
from core.events.product_received import ProductReceivedEvent
from core.telemetry.logger import logger
from core.telemetry.metrics import MESSAGES_TOTAL
from prometheus_client import start_http_server
from core.config.settings import settings
import uuid
import re
import os

URL_REGEX = r"(https?://[^\s]+)"

publisher = RabbitPublisher()

start_http_server(8001)

async def handle_message(
update: Update,
context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    urls = re.findall(URL_REGEX, text)

    if not urls:
        return

    for url in urls:

        correlation_id = str(uuid.uuid4())

        event = ProductReceivedEvent(
            correlation_id=correlation_id,
            url=url,
            source="telegram",
            chat_id=update.effective_chat.id
        )

        await publisher.publish(
            "product.received",
            event
        )

        MESSAGES_TOTAL.inc()

        logger.info(
            "Evento publicado",
            extra={
                "service": "bot",
                "correlation_id": correlation_id
            }
        )

        await update.message.reply_text(
            "✅ Link enviado"
        )

app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
