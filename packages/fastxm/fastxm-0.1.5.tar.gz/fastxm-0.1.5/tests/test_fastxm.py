import string
import numpy as np
from fastxm import intersect_1d

size = 10_000
iters = 50

a1k = np.random.choice(10_000, size=1_000, replace=False)
a100k = np.random.choice(1_000_000, size=100_000, replace=False)
a5m = np.random.choice(20_000_000, size=5_000_000, replace=False)

b1k = np.random.choice(10_000, size=1_000, replace=False)
b100k = np.random.choice(1_000_000, size=100_000, replace=False)
b5m = np.random.choice(20_000_000, size=5_000_000, replace=False)

s50k1 = np.random.choice(list(string.ascii_lowercase), size=50_000)
s50k2 = np.random.choice(list(string.ascii_lowercase), size=50_000)

s50k10_1 = np.array(
    [
        "".join(i)
        for i in np.random.choice(list(string.ascii_lowercase), size=(50_000, 10))
    ]
)
s50k10_2 = np.array(
    [
        "".join(i)
        for i in np.random.choice(list(string.ascii_lowercase), size=(50_000, 10))
    ]
)


def test_same_as_numpy():

    for _ in range(iters):
        a = np.random.choice(size * 10, size=size, replace=False)
        b = np.random.choice(size * 10, size=size, replace=False)

        i1, j1 = intersect_1d(a, b)
        i2, j2 = np.intersect1d(a, b, return_indices=True, assume_unique=True)[1:]

        assert np.all(np.equal(np.sort(i1), np.sort(i2)))
        assert np.all(np.equal(np.sort(j1), np.sort(j2)))


def test_1k_i1d(benchmark):
    benchmark(intersect_1d, a1k, b1k)


def test_1k_i1d_par(benchmark):
    benchmark(intersect_1d, a1k, b1k, parallel=True)


def test_1k_numpy(benchmark):
    benchmark(np.intersect1d, a1k, b1k, return_indices=True, assume_unique=True)


def test_100k_i1d(benchmark):
    benchmark(intersect_1d, a100k, b100k)


def test_100k_i1d_par(benchmark):
    benchmark(intersect_1d, a100k, b100k, parallel=True)


def test_100k_numpy(benchmark):
    benchmark(np.intersect1d, a100k, b100k, return_indices=True, assume_unique=True)


def test_5m_i1d(benchmark):
    benchmark(intersect_1d, a5m, b5m)


def test_5m_i1d_par(benchmark):
    benchmark(intersect_1d, a5m, b5m, parallel=True)


def test_5m_numpy(benchmark):
    benchmark(np.intersect1d, a5m, b5m, return_indices=True, assume_unique=True)


def test_smallbig_i1d(benchmark):
    benchmark(intersect_1d, a5m, b100k)


def test_smallbig_i1d_par(benchmark):
    benchmark(intersect_1d, a5m, b100k, parallel=True)


def test_bigsmall_i1d(benchmark):
    benchmark(intersect_1d, a100k, b5m)


def test_bigsmall_i1d_par(benchmark):
    benchmark(intersect_1d, a100k, b5m, parallel=True)


def test_string_numpy_50k10(benchmark):
    benchmark(
        np.intersect1d, s50k10_1, s50k10_2, return_indices=True, assume_unique=True
    )


def test_string_fastxm_50k10(benchmark):
    benchmark(intersect_1d, s50k10_1, s50k10_2)


def test_string_fastxm_50k10_par(benchmark):
    benchmark(intersect_1d, s50k10_1, s50k10_2, parallel=True)
