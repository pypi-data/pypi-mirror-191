from abc import ABC, abstractmethod
from decimal import Decimal


class AbstractLiability(ABC):
    _bands: None

    @property
    @abstractmethod
    def taxable_amount(self):
        return NotImplementedError

    @property
    @abstractmethod
    def total(self):
        return NotImplementedError

    @property
    def breakdown(self) -> [tuple[Decimal, Decimal, Decimal]]:
        return (
            (a, b, a * b / 100) for a, b in self._bands.allocate(self.taxable_amount)
        )

    @property
    def _minimum(self):
        return NotImplementedError
