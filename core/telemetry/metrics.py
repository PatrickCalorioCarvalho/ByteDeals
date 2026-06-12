from prometheus_client import Counter
from prometheus_client import Histogram

BOT_MESSAGES_RECEIVED = Counter(
    "bot_messages_received_total",
    "Mensagens recebidas pelo bot"
)

BOT_URLS_RECEIVED = Counter(
    "bot_urls_received_total",
    "URLs recebidas pelo bot"
)

BOT_EVENTS_PUBLISHED = Counter(
    "bot_events_published_total",
    "Eventos publicados pelo bot"
)

BOT_INVALID_MESSAGES = Counter(
    "bot_invalid_messages_total",
    "Mensagens sem URL"
)

BOT_PROCESSING_TIME = Histogram(
    "bot_processing_seconds",
    "Tempo processamento do bot"
)

PRODUCT_RECEIVED_TOTAL = Counter(
    "product_received_total",
    "Produtos recebidos pelo extractor"
)

PRODUCT_EXTRACTED_TOTAL = Counter(
    "product_extracted_total",
    "Produtos extraídos com sucesso"
)

EXTRACTOR_ERRORS_TOTAL = Counter(
    "extractor_errors_total",
    "Falhas durante extração"
)

EXTRACTOR_PROCESSING_TIME = Histogram(
    "extractor_processing_seconds",
    "Tempo processamento extractor"
)

PRODUCT_ENRICHED_TOTAL = Counter(
    "product_enriched_total",
    "Produtos enriquecidos pela IA"
)

AI_REQUESTS_TOTAL = Counter(
    "ai_requests_total",
    "Chamadas realizadas para a IA"
)

AI_ERRORS_TOTAL = Counter(
    "ai_errors_total",
    "Falhas na geração IA"
)

AI_GENERATION_TIME = Histogram(
    "ai_generation_seconds",
    "Tempo geração IA"
)

PRODUCT_PUBLISHED_TOTAL = Counter(
    "product_published_total",
    "Mensagens publicadas"
)

PUBLISHER_ERRORS_TOTAL = Counter(
    "publisher_errors_total",
    "Falhas no envio"
)

PUBLISHER_PROCESSING_TIME = Histogram(
    "publisher_processing_seconds",
    "Tempo processamento publisher"
)

RABBIT_MESSAGES_PUBLISHED = Counter(
    "rabbit_messages_published_total",
    "Mensagens publicadas no RabbitMQ"
)

RABBIT_MESSAGES_CONSUMED = Counter(
    "rabbit_messages_consumed_total",
    "Mensagens consumidas do RabbitMQ"
)


EVENTS_TOTAL = Counter(
    "events_total",
    "Total de eventos processados"
)

ERRORS_TOTAL = Counter(
    "errors_total",
    "Total de erros"
)

PROCESSING_TIME = Histogram(
    "processing_seconds",
    "Tempo geral de processamento"
)