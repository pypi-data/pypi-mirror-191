from decimal import Decimal
from itertools import accumulate
from typing import Any, Callable


def step(amount: Decimal, bands: list[Decimal]) -> tuple[tuple[Decimal, Any], ...]:
    """
    Step liabilities work by allocating the amount to the incremental thresholds
    of a given band, in order, until nothing is left.
    """

    def allocable(amount: Decimal) -> Callable[[Decimal], Decimal]:
        def allocate_to(threshold):
            nonlocal amount
            allocation = min(amount, threshold)
            amount -= allocation
            return allocation

        return allocate_to

    allocable_amount = allocable(amount)
    return tuple((allocable_amount(t), p) for t, p in bands)


def slab(amount: Decimal, bands: list[Decimal]) -> tuple[tuple[Decimal, Any], ...]:
    """
    Slab liabilities work by comparing the provided amount with the *cumulative*
    threshold of a given band.
    When the amount first exceeds a cumulative threshold of a band,
    all the amount is allocated to that band.
    """

    bands = zip(accumulate(t for t, _ in bands), (p for _, p in bands))

    def allocable(amount: Decimal) -> Callable[[Decimal], Decimal]:
        def allocate_to(threshold):
            nonlocal amount
            if amount > threshold:
                return Decimal("0")
            allocation, amount = amount, Decimal("0")
            return allocation

        return allocate_to

    allocable_amount = allocable(amount)
    return tuple((allocable_amount(t), p) for t, p in bands)
