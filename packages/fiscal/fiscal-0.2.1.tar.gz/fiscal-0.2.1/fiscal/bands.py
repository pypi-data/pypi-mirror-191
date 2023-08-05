from .abstract_bands import AbstractBands
from .allocators import slab, step


class SlabbedBands(AbstractBands):
    @property
    def _allocator(self):
        return slab


class SteppedBands(AbstractBands):
    @property
    def _allocator(self):
        return step
