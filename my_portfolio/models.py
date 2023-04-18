from datetime import datetime


class Visitor:
    def __init__(self, ip_address, city, country, message):
        self.ip_address = ip_address
        self.city = city
        self.country = country
        self.message = message
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            'ip_address': self.ip_address,
            'city': self.city,
            'country': self.country,
            'message': self.message,
            'timestamp': self.timestamp
        }
