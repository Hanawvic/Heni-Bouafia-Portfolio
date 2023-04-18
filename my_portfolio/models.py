import uuid
from datetime import datetime


class Visitor:
    def __init__(self, message):
        self.message = message
        self.id = uuid.uuid4().hex
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': self.id,
            'message': self.message,
            'timestamp': self.timestamp
        }
