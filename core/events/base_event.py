from pydantic import BaseModel
from datetime import datetime
import uuid

class BaseEvent(BaseModel):
    event_id: str = str(uuid.uuid4())
    timestamp: str = datetime.utcnow().isoformat()
    correlation_id: str
