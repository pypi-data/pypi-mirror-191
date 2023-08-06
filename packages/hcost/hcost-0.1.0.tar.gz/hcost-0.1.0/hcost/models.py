import doctest
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict

from hcost.utils import format_decimal


@dataclass
class Tenant:
    """
    A simple class to abstract a tenant with some helper methods.

    >>> now = datetime.now()
    >>> last_year = now - timedelta(days=365)
    >>> next_year = now + timedelta(days=365)
    >>> now_delivery = Tenant("Foo", "Guy", Decimal("100.00"), last_year, next_year)
    >>> assert last_year <= now_delivery <= next_year
    >>> assert not (last_year < now_delivery < next_year)
    """

    first_name: str
    last_name: str
    area: Decimal
    start_rent: datetime
    end_rent: datetime | None

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self.start_rent > other

        raise ValueError(f"{other} is not from type datetime")

    def __lt__(self, other):
        if not self.end_rent:
            return False

        if isinstance(other, datetime):
            return self.end_rent < other

        raise ValueError(f"{other} is not from type datetime")

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self.start_rent >= other

        raise ValueError(f"{other} is not from type datetime")

    def __le__(self, other):
        if not self.end_rent:
            return False

        if isinstance(other, datetime):
            return self.end_rent <= other

        raise ValueError(f"{other} is not from type datetime")


@dataclass
class Delivery:
    """
    A simple class to abstract an oil delivery with some helper methods.

    >>> now = datetime.now()
    >>> yesterday = now - timedelta(days=1)
    >>> tomorrow = now + timedelta(days=1)
    >>> now_delivery = Delivery(Decimal("1000.00"), Decimal("13.37"), now)
    >>> assert yesterday < now_delivery < tomorrow
    >>> assert yesterday <= now_delivery <= tomorrow
    """

    liters: Decimal
    netto_price: Decimal
    date: datetime

    @property
    def total(self) -> Decimal:
        return self.liters * self.netto_price

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self.date >= other

        if isinstance(other, Delivery):
            return self.date >= other.date

        raise ValueError(f"{other} is not from type Delivery or datetime")

    def __le__(self, other):
        if isinstance(other, datetime):
            return self.date <= other

        if isinstance(other, Delivery):
            return self.date <= other.date

        raise ValueError(f"{other} is not from type Delivery or datetime")

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self.date > other

        if isinstance(other, Delivery):
            return self.date > other.date

        raise ValueError(f"{other} is not from type Delivery or datetime")

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self.date < other

        if isinstance(other, Delivery):
            return self.date < other.date

        raise ValueError(f"{other} is not from type Delivery or datetime")

    def __str__(self):
        return f"{self.date.isoformat()}\t::\t{format_decimal(self.liters)}l\t::\t{format_decimal(self.netto_price)}€"


@dataclass
class Bill:
    total_area: Decimal
    tenants: Dict[str, Tenant]
    deliveries: List[Delivery]


class TenantNotFound(Exception):
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id

    def __str__(self):
        return f"Could not find {self.tenant_id}"


if __name__ == '__main__':
    doctest.testmod()
