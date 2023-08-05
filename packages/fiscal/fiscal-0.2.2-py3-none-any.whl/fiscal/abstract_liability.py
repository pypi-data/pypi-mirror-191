from abc import ABC, abstractmethod
from decimal import Decimal


class AbstractLiability(ABC):

    """
    Basis for liabilities to be calculated.
    """

    _bands: None

    @property
    @abstractmethod
    def taxable_amount(self):
        return NotImplementedError

    @property
    @abstractmethod
    def total(self):
        """
        Should return the sum of any liabilitis in the breakdown
        """
        return NotImplementedError

    @property
    def breakdown(self) -> [tuple[Decimal, Decimal, Decimal]]:
        """
        Will produce the product of an allocated band and its rate
        alongside both.
        """
        return (
            (a, b, a * b / 100) for a, b in self._bands.allocate(self.taxable_amount)
        )

    @property
    def _minimum(self):
        """
        Sets the minimum liability applicable
        """

        return NotImplementedError
