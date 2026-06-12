from pydantic import BaseModel, Field
from core.utils.ids import generate_id
from core.utils.datetime import utc_now


class BaseEvent(BaseModel):

    event_id: str = Field(
        default_factory=generate_id
    )
    timestamp: str = Field(
        default_factory=utc_now
    )
    correlation_id: str
    trace_id: str | None = None
    source_service: str