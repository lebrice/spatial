from __future__ import annotations
import typing
from typing import Any

from .space import Space
from .spatial import Discrete as _Discrete

if typing.TYPE_CHECKING:
    # NOTE: Seems like type checkers aren't yet able to check this.
    from .space import PositiveInt


__all__ = ["Discrete"]


class Discrete[I: PositiveInt](Space[I]):
    n: I
    def __init__(self, n: I, rng_seed: int | None = None):
        super().__init__()
        self.n = n
        self._discrete = _Discrete(n, rng_seed=rng_seed)

    def sample(self) -> I:
        return self._discrete.sample()
    
    def sample_batch(self, num_samples: PositiveInt) -> list[I]:
        return self._discrete.sample_batch(num_samples)

    def contains(self, v: Any) -> bool:
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


