"""Tests for `spatial` package."""

import pytest

from spatial import Discrete


def test_discrete():
    space = Discrete(10)
    assert space.sample() in range(10)
    assert isinstance(space.sample(), int)
    # Test that it's roughly uniform.
    assert set(space.sample() for _ in range(100)) == set(range(10))


def test_positive_int_annotation_warns_of_error():
    # The type checker doesn't seem to be able to use the `annotated_types` stuff yet.
    with pytest.raises(OverflowError, match="can't convert negative int to unsigned"):
        Discrete(-123)


def test_bad_arguments_to_methods():
    with pytest.raises(
        OverflowError, match="can't convert negative int to unsigned"
    ):
        _ = Discrete(-1)

    with pytest.raises(OverflowError, match="can't convert negative int to unsigned"):
        Discrete(10).sample_batch(-123)

    with pytest.raises(
        TypeError,
        match="argument 'n': 'str' object cannot be interpreted as an integer",
    ):
        Discrete("123")

    with pytest.raises(
        TypeError,
        match="argument 'n': 'float' object cannot be interpreted as an integer",
    ):
        Discrete(10).sample_batch(1.23)


def test_same_seed_same_values():
    n_values = 100
    n = 10
    seed = 123
    space = Discrete(n, rng_seed=seed)
    values = list(space.sample() for _ in range(n_values))

    same_seed_space = Discrete(n, rng_seed=seed)
    same_seed_values = list(same_seed_space.sample() for _ in range(n_values))
    assert values == same_seed_values


def test_different_seed_different_values():
    n_values = 100
    n = 10
    space = Discrete(n, rng_seed=123)
    values = list(space.sample() for _ in range(n_values))

    different_seed_space = Discrete(n, rng_seed=456)
    different_values = list(different_seed_space.sample() for _ in range(n_values))
    assert values != different_values


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


def test_contains():
    n = 10
    space = Discrete(n, rng_seed=123)

    assert 3 in space
    assert 3.12 not in space
    assert 10 not in space
    assert 0 in space
    assert 123 not in space
    assert "bob" not in space

def test_repr():
    assert str(Discrete(10)) == "Discrete(10)"