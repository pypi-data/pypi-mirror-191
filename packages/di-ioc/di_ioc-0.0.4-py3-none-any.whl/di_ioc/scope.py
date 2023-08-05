import logging
from typing import Callable, List

from .abstraction import AbstractScope

log = logging.getLogger(__name__)


class ServiceScope(AbstractScope):
    def __init__(self):
        self._cleanup: List[Callable[['ServiceScope'], None]] = []

    @property
    def on_dispose(self) -> List[Callable[['ServiceScope'], None]]:
        return self._cleanup

    def dispose(self):
        log.debug(f'cleaning {len(self._cleanup)} services in scope')
        for d in self._cleanup:
            d(self)
        self._cleanup.clear()
