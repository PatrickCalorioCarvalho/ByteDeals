from core.events.base_event import BaseEvent

class ProductReceivedEvent(BaseEvent):
    url: str
    source: str
    chat_id: int