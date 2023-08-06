from datetime import (
    datetime, )
from decimal import (
    Decimal,
)
from doctest import (
    testmod,
)
from logging import (
    Logger, getLogger, DEBUG, StreamHandler,
)
from random import (
    Random,
)
from sys import (
    stdout,
)
from typing import Dict

from dateutil.parser import parse

from hcost.models import (
    Bill, TenantNotFound, Delivery,
)
from hcost.utils import (
    readj, deterministic_uuid
)

L = getLogger(__name__)
L.setLevel(DEBUG)
handler = StreamHandler(stdout)
handler.setLevel(DEBUG)
L.addHandler(handler)


def create_bill(raw: Dict, seed: int = 1337) -> Bill:
    r = Random(seed)
    return Bill(**{
        **raw,
        "tenants": {
            str(deterministic_uuid(r)): tenant for tenant in raw.get("tenants")
        }
    })


def create_bill_from_path(path: str, seed: int = 1337) -> Bill:
    raw = readj(path)
    return create_bill(raw, seed)


def get_tenant_cost(
        bill: Bill,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime,
        logger: Logger = None
) -> Decimal:
    """
    >>> from hcost.models import Tenant
    >>> from hcost.utils import get_first_of_year, get_next_year
    >>> this_year = get_first_of_year(2023)
    >>> next_year = get_next_year(this_year)
    >>> now = parse("2023-02-13T02:38:40.024512")
    >>> fake_tenants = {"alibaba": Tenant("Ali", "Baba", Decimal("50.00"), this_year, now,), }
    >>> bill = Bill(Decimal("50"),fake_tenants, [Delivery(Decimal("123"), Decimal("13.37"), now), Delivery(Decimal("123"), Decimal("13.37"), now)])
    >>> get_tenant_cost(bill, "alibaba", this_year, next_year)
    Decimal('462.2751014546659430022840231')

    :param bill:
    :param tenant_id:
    :param start_date:
    :param end_date:
    :param logger:
    :return:
    """
    if not logger:
        logger = L

    tenant = bill.tenants.get(tenant_id)
    if not tenant:
        logger.error("Could not find tenant with id: %s", tenant_id)
        raise TenantNotFound(tenant_id)

    logger.debug("Looking for relevant deliveries between: %s to %s", start_date, end_date)

    relevant_deliveries = [
        delivery for delivery in bill.deliveries
        if start_date <= delivery <= end_date
    ]

    logger.debug("Relevant deliveries are:\n\t%s", "\n\t".join(map(str, relevant_deliveries)))

    total_costs = sum((delivery.netto_price * Decimal("1.19") * delivery.liters for delivery in relevant_deliveries))
    logger.debug("Total cost of all deliveries are: %s €", total_costs)
    logger.debug("Total area is: %s m²", bill.total_area)

    delta_time = end_date - start_date
    tenant_end_rent = tenant.end_rent or end_date  # if tenant still lives there
    tenant_time = min(tenant_end_rent, end_date) - max(tenant.start_rent, start_date)
    logger.debug("Time frame that we consider: %s", delta_time)
    logger.debug(
        "Time frame of rent we consider for tenant %s %s: %s",
        tenant.first_name,
        tenant.last_name,
        tenant_time,
    )

    time_factor = Decimal(tenant_time / delta_time)
    area_factor = Decimal(tenant.area / bill.total_area)

    costs = time_factor * area_factor * total_costs
    logger.debug("The costs for the tenant %s %s are: %s€", tenant.first_name, tenant.last_name, costs)
    return costs


if __name__ == '__main__':
    testmod()
