from __future__ import annotations

import typing
from typing import Any, TypeVar, overload

from typing_extensions import TypeVar

from .space import Space
from .spatial import Discrete as _Discrete

if typing.TYPE_CHECKING:
    from .space import PositiveInt


__all__ = ["Discrete"]


class Discrete[I: int](Space[I]):
    @overload
    def __init__(
        self,
        *,
        start: I,
        n: I,
        rng_seed: int | None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        n: PositiveInt,
        *,
        start: None = None,
        rng_seed: int | None = None,
    ):
        ...

    def __init__(
        self,
        n: I | PositiveInt,
        *,
        start: I | None = None,
        rng_seed: int | None = None,
    ):
        super().__init__()
        self.n = n
        self.start = start
        if self.start is not None:
            assert self.n > self.start
        self._discrete = _Discrete(
            self.n - self.start if self.start is not None else self.n, rng_seed=rng_seed
        )

    def sample(self) -> I:
        if self.start is None:
            return self._discrete.sample()
        return self.start + self._discrete.sample()

    def sample_batch(self, num_samples: PositiveInt) -> list[I]:
        batch = self._discrete.sample_batch(num_samples)
        if self.start is None:
            return batch
        return [self.start + v for v in batch]

    def contains(self, v: Any) -> bool:
        if self.start is not None:
            v = v - self.start
        v = self._discrete.contains(v)
        assert isinstance(v, bool)
        return v

    def __contains__(self, v: Any) -> bool:
        if not isinstance(v, type(self.n)):
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
        if self.start is None:
            return f"{type(self).__name__}({self.n})"

        return f"{type(self).__name__}(start={self.start}, n={self.n})"

        # def without_self(v_str: str):
        #     return v_str.removeprefix("self.")

        # return f"{type(self).__name__}({without_self(f"{self.start=}")}, {without_self(f"{self.n=}")})"
