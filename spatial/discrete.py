from __future__ import annotations
import typing
from typing import Any, TypeVar

from .space import Space
from .spatial import Discrete as _Discrete

if typing.TYPE_CHECKING:
    from .space import PositiveInt


__all__ = ["Discrete"]


class Discrete[I: int](Space[I]):
    def __init__(
        self, n: PositiveInt, rng_seed: int | None = None, start: I | None = None
    ):
        super().__init__()
        if start is not None:
            assert n > start, (n, start)
            n = n - start
        self.n = n
        self.start = start or 0
        self._discrete = _Discrete(n, rng_seed=rng_seed)

    def sample(self) -> I:
        return self.start + self._discrete.sample()

    def sample_batch(self, num_samples: PositiveInt) -> list[I]:
        batch = self._discrete.sample_batch(num_samples)
        if not self.start:
            return batch
        return [self.start + v for v in batch]

    def contains(self, v: Any) -> bool:
        if self.start:
            v = v - self.start
        return self._discrete.contains(v)

    def __contains__(self, v: Any) -> bool:
        if not isinstance(v, int):
            return False
        try:
            int_val = int(v)
        except TypeError:
            return False
        else:
            if int_val != v:
                return False
        return self.contains(v)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.n})"
