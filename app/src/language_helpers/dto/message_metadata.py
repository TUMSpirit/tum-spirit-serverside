from datetime import datetime

class Metadata():
    sentiment: dict
    flesh_reading_ease: float
    MTBI: dict
    OCEAN: dict


class MessageMetadata():
    id: str
    message_id: str
    timestamp: datetime
    metadata: Metadata
