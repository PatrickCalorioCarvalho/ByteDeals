from prometheus_client import Counter, Histogram

MESSAGES_TOTAL = Counter(
"messages_total",
"Mensagens processadas"
)

PROCESSING_TIME = Histogram(
"processing_time_seconds",
"Tempo de processamento"
)
