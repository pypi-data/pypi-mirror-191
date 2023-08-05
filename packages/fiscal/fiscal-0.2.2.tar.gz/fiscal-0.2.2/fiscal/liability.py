from decimal import Decimal

from .abstract_bands import AbstractBands
from .abstract_liability import AbstractLiability


class Liability(AbstractLiability):
    def __init__(self, bands: AbstractBands, taxable_amount: int | float | Decimal):
        self._bands = bands
        self._taxable_amount = Decimal(taxable_amount)

    @property
    def taxable_amount(self):
        return self._taxable_amount

    @property
    def total(self):
        return sum((liab for _, _, liab in self.breakdown))

    @property
    def _minimum(self):
        return Decimal("0")
