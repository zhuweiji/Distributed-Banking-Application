from enum import Enum


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    SGD = 'SGD'

    @classmethod
    def get_available(cls):
        return list(map(lambda c: c.value, cls))

