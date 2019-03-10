#!/usr/bin/env python3
# Piotr Beling, 2019

def primes():
    """Generate prime numbers ad infinitum using Sieve of Eratosthenes algorithm."""
    p = {}
    n = 2
    while True:
        l = p.get(n)
        if l is None:
            yield n
            l = [n]
        else:
            del p[n]
        for v in l:
            # add v to p[n+v] list
            k = n+v
            dest = p.get(k)
            if dest is None:
                p[k] = [v]
            else:
                dest.append(v)
        n += 1

if __name__ == "__main__": # demo program:
    from itertools import takewhile
    for prime in takewhile(lambda x: x < 100, primes()):
        print(prime)
