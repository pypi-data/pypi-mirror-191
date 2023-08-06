from enum import StrEnum


class Currency(StrEnum):
    USD: str = "USD"
    RUB: str = "RUB"
    EUR: str = "EUR"

    @classmethod
    def from_name(cls, name: str):
        name = name.upper()
        for i in Currency:
            if i == name:
                return i
        return None



