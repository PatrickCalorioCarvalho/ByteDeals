from contextvars import ContextVar


correlation_id_ctx = ContextVar(
    "correlation_id",
    default=None
)

trace_id_ctx = ContextVar(
    "trace_id",
    default=None
)

event_id_ctx = ContextVar(
    "event_id",
    default=None
)

service_ctx = ContextVar(
    "service",
    default=None
)

routing_key_ctx = ContextVar(
    "routing_key",
    default=None
)

chat_id_ctx = ContextVar(
    "chat_id",
    default=None
)


def set_context(
    correlation_id=None,
    trace_id=None,
    event_id=None,
    service=None,
    routing_key=None,
    chat_id=None
):

    if correlation_id:
        correlation_id_ctx.set(
            correlation_id
        )

    if trace_id:
        trace_id_ctx.set(
            trace_id
        )

    if event_id:
        event_id_ctx.set(
            event_id
        )

    if service:
        service_ctx.set(
            service
        )

    if routing_key:
        routing_key_ctx.set(
            routing_key
        )

    if chat_id:
        chat_id_ctx.set(
            chat_id
        )


def get_context():

    return {
        "correlation_id":
            correlation_id_ctx.get(),

        "trace_id":
            trace_id_ctx.get(),

        "event_id":
            event_id_ctx.get(),

        "service":
            service_ctx.get(),

        "routing_key":
            routing_key_ctx.get(),

        "chat_id":
            chat_id_ctx.get()
    }