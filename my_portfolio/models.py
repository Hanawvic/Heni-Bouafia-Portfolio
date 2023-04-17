from datetime import datetime


class Visitor:
    def __init__(self, ip_address, city, country, internet_provider, message):
        self.ip_address = ip_address
        self.city = city
        self.country = country
        self.internet_provider = internet_provider
        self.message = message
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            'ip_address': self.ip_address,
            'city': self.city,
            'country': self.country,
            'isp': self.internet_provider,
            'message': self.message,
            'timestamp': self.timestamp
        }
