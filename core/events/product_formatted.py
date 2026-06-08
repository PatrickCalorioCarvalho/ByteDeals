from core.events.base_event import BaseEvent

class ProductFormattedEvent(BaseEvent):
    chat_id: int
    title: str
    image: str
    link: str
    message: str
