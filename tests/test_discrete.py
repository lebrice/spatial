"""Tests for `spatial` package."""

import pytest

from spatial import Discrete


def test_sample():
    n = 10
    space = Discrete(n)
    assert space.n == n
    assert space.sample() in range(n)
    assert isinstance(space.sample(), int)
    # Test that it's roughly uniform.
    assert set(space.sample() for _ in range(n * 10)) == set(range(n))


def test_sample_batch():
    n = 10
    n_values = 100
    space = Discrete(n, rng_seed=123)

    values = space.sample_batch(n_values)
    assert isinstance(values, list)
    assert all(isinstance(v, int) for v in values)
    assert len(values) == n_values
    assert min(values) >= 0
    assert max(values) < n
    assert n // 2 < len(set(values)) <= n


def test_positive_int_annotation_warns_of_error():
    # The type checker doesn't seem to be able to use the `annotated_types` stuff yet.
    with pytest.raises(OverflowError, match="can't convert negative int to unsigned"):
        Discrete(-123)


def test_bad_arguments_to_methods():
    with pytest.raises(OverflowError, match="can't convert negative int to unsigned"):
        _ = Discrete(-1)

    with pytest.raises(OverflowError, match="can't convert negative int to unsigned"):
        Discrete(10).sample_batch(-123)

    with pytest.raises(
        TypeError,
        match="argument 'n': 'str' object cannot be interpreted as an integer",
    ):
        Discrete("123")  # type: ignore

    with pytest.raises(
        TypeError,
        match="argument 'n': 'float' object cannot be interpreted as an integer",
    ):
        Discrete(10).sample_batch(1.23)  # type: ignore


def test_sample_same_seed_same_values():
    n_values = 100
    n = 10
    seed = 123
    space = Discrete(n, rng_seed=seed)
    values = list(space.sample() for _ in range(n_values))

    same_seed_space = Discrete(n, rng_seed=seed)
    same_seed_values = list(same_seed_space.sample() for _ in range(n_values))
    assert values == same_seed_values


def test_sample_different_seed_different_values():
    n_values = 100
    n = 10
    space = Discrete(n, rng_seed=123)
    values = list(space.sample() for _ in range(n_values))

    different_seed_space = Discrete(n, rng_seed=456)
    different_values = list(different_seed_space.sample() for _ in range(n_values))
    assert values != different_values


def test_sample_batch_same_seed_same_values():
    n_values = 100
    n = 10
    seed = 123
    space = Discrete(n, rng_seed=seed)
    values = space.sample_batch(n_values)

    same_seed_space = Discrete(n, rng_seed=seed)
    same_seed_values = same_seed_space.sample_batch(n_values)
    assert values == same_seed_values


def test_sample_batch_different_seed_different_values():
    n_values = 100
    n = 10
    space = Discrete(n, rng_seed=123)
    values = space.sample_batch(n_values)

    different_seed_space = Discrete(n, rng_seed=456)
    different_values = different_seed_space.sample_batch(n_values)
    assert values != different_values


def test_foo():
    assert 1 in Discrete(10)
    assert 0 in Discrete(10)


@pytest.mark.parametrize(
    ("start", "n", "v", "expected"),
    [
        (None, 10, 0, True),
        (None, 10, 1, True),
        (None, 10, 10, False),
        (None, 10, 0.2, False),
        (None, 10, "bob", False),
        (None, 1, 0, True),
        (0, 10, 0, True),
        (0, 10, 1, True),
        (0, 10, 10, False),
        (0, 10, 0.2, False),
        (0, 10, "bob", False),
        (0, 1, 0, True),
        (-10, 10, -10, True),
        (-10, 10, -5, True),
        (-10, 10, 9, True),
        (-10, 10, 10, False),
        (-10, 10, 0.2, False),
        (-10, 10, "bob", False),
        (-10, 1, 0, True),
    ],
)
def test_contains(start: int | None, n: int, v: int, expected: bool):
    space = Discrete(start=start, n=n, rng_seed=123)
    assert (v in space) == expected, (space, v, v in space, expected)


def test_repr():
    assert str(Discrete(10)) == "Discrete(10)"


def test_discrete_with_start():
    n_values = 100
    n = 10
    start = 2
    space = Discrete(
        start=start,
        n=n,
        rng_seed=123,
    )
    for values in [
        space.sample_batch(n_values),
        [space.sample() for _ in range(n_values)],
    ]:
        assert all(start <= v <= n for v in values)


def test_repr_with_start():
    assert str(Discrete(n=10, start=2)) == "Discrete(start=2, n=10)"


@pytest.mark.xfail(reason="Not sure if we want to support the `dtype` param as in gym.")
def test_discrete_with_numpy_types():
    import numpy as np

    dtype = np.int16

    n_values = 100
    n = np.array([10]).item()
    n: dtype = dtype(10)
    start: dtype = dtype(2)
    space: Discrete[dtype] = Discrete(
        start=start,
        n=n,
        rng_seed=123,
    )
    for values in [
        space.sample_batch(n_values),
        [space.sample() for _ in range(n_values)],
    ]:
        assert all(start <= v <= n for v in values)
        assert all(isinstance(v, dtype) for v in values)
