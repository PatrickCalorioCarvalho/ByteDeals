from core.events.base_event import BaseEvent

class ProductEnrichedEvent(BaseEvent):
    chat_id: int
    title: str
    image: str
    link: str
    old_price: str | None = None
    new_price: str | None = None
    discount: int | None = None
    economy: str | None = None
    ai_text: str | None = None
