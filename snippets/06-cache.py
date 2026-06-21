from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def primes(limit: int) -> list[int]:
    sieve = [True] * limit
    out = []
    for i in range(2, limit):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, limit, i):
                sieve[j] = False
    return out


print(fib(20), primes(30))
