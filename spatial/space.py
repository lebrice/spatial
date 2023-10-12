from __future__ import annotations
import typing

from typing import Protocol

if typing.TYPE_CHECKING:
    from typing import Annotated, Any, Sequence
    from annotated_types import Gt

    # NOTE: Seems like type checkers aren't yet able to check this.
    PositiveInt = Annotated[int, Gt(0)]

__all__ = ["Space"]


class Space[T_co](Protocol):
    def sample(self) -> T_co:
        raise NotImplementedError

    def sample_batch(self, num_samples: PositiveInt) -> Sequence[T_co]:
        raise NotImplementedError

    def contains(self, v: Any) -> bool:
        raise NotImplementedError

    def __contains__(self, v: Any) -> bool:
        return self.contains(v)
