from typing import Annotated, Any

from annotated_types import Gt

PositiveInt = Annotated[int, Gt(0)]

class Discrete:
    n: int
    def __init__(self, n: PositiveInt, rng_seed: int | None = None):
        ...
    def sample(self) -> int:
        ...
    def sample_batch(self, n: PositiveInt) -> list[int]:
        ...

    def contains(self, v: Any) -> bool:
        ...

    def __contains__(self, v: Any) -> bool:
        ...
    
    def __repr__(self) -> str:
        ...
