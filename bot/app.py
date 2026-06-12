from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

from prometheus_client import start_http_server

from core.config.settings import settings
from core.rabbit.publisher import RabbitPublisher

from core.events.product_received import (
    ProductReceivedEvent
)

from core.telemetry.logger import logger
from core.telemetry.context import set_context

from core.telemetry.metrics import (
    BOT_MESSAGES_RECEIVED,
    BOT_URLS_RECEIVED,
    BOT_EVENTS_PUBLISHED,
    BOT_INVALID_MESSAGES,
    BOT_PROCESSING_TIME
)

import re
import uuid

URL_REGEX = r"(https?://[^\s]+)"

publisher = RabbitPublisher()

start_http_server(8001)


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    with BOT_PROCESSING_TIME.time():

        BOT_MESSAGES_RECEIVED.inc()

        text = update.message.text

        logger.info(
            "Mensagem recebida",
            extra={
                "chat_id": update.effective_chat.id
            }
        )

        urls = re.findall(
            URL_REGEX,
            text
        )

        if not urls:

            BOT_INVALID_MESSAGES.inc()

            logger.warning(
                "Mensagem ignorada - nenhuma URL encontrada"
            )

            return

        for url in urls:

            BOT_URLS_RECEIVED.inc()

            correlation_id = str(
                uuid.uuid4()
            )

            trace_id = str(
                uuid.uuid4()
            )

            set_context(
                correlation_id=correlation_id,
                trace_id=trace_id,
                service="bot"
            )

            logger.info(
                "URL encontrada",
                extra={
                    "url": url
                }
            )

            event = ProductReceivedEvent(
                correlation_id=correlation_id,
                trace_id=trace_id,
                source_service="bot",
                url=url,
                source="telegram",
                chat_id=update.effective_chat.id
            )

            await publisher.publish(
                "product.received",
                event
            )

            BOT_EVENTS_PUBLISHED.inc()

            logger.info(
                "Evento publicado"
            )

            await update.message.reply_text(
                "✅ Link enviado para processamento"
            )


logger.info(
    "Bot iniciando"
)

app = (
    ApplicationBuilder()
    .token(settings.TELEGRAM_TOKEN)
    .build()
)

app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle_message
    )
)

logger.info(
    "Bot iniciado"
)

app.run_polling()