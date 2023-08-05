import abc
from decimal import Decimal
from functools import partial
from typing import Callable, Tuple


class AbstractBands(abc.ABC):
    """
    Accepts a tuple of two-tuples.
    Each two-tuple comprises two number-like elements:
    a) an incremental threshold, and
    b) a percentage that applies until that incremental threshold is breached.
    """

    def __init__(
        self,
        values: Tuple[Tuple[Decimal | int | float, Decimal | int | float], ...],
    ) -> None:
        self._values = tuple(
            (Decimal(threshold), Decimal(percentage))
            for threshold, percentage in values
        )

    @property
    def _allocator(self):
        return NotImplementedError

    @property
    def allocate(self) -> Callable:
        return partial(self._allocator, bands=self.values)

    @property
    def values(self) -> Tuple[Tuple[Decimal, Decimal], ...]:
        return self._values
