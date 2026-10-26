"""Finite, falsifiable tests of 6k±1 Goldbach index hypotheses.

No test in this module is evidence of a universal Goldbach proof.
"""

import math
import unittest


def primes_up_to(limit):
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if is_prime[p]:
            is_prime[p * p:limit + 1:p] = b"\0" * (((limit - p * p) // p) + 1)
    return is_prime, [p for p in range(2, limit + 1) if is_prime[p]]


def index_of_prime_gt_three(p):
    assert p > 3 and p % 6 in (1, 5)
    return (p - 1) // 6 if p % 6 == 1 else (p + 1) // 6


def goldbach_pairs_gt_three(n, is_prime, primes):
    for p in primes:
        if p > n // 2:
            break
        if p > 3 and is_prime[n - p]:
            yield (p, n - p)


class TestGoldbachIndexExperiment(unittest.TestCase):
    LIMIT = 20_000

    @classmethod
    def setUpClass(cls):
        cls.is_prime, cls.primes = primes_up_to(cls.LIMIT)

    def test_index_sum_identity_for_every_checked_prime_pair(self):
        """The identities hold for every found representation up to LIMIT."""
        for n in range(10, self.LIMIT + 1, 2):
            pairs = list(goldbach_pairs_gt_three(n, self.is_prime, self.primes))
            self.assertTrue(pairs, f"No representation using primes >3 at n={n}")
            total = n // 6 + (n % 6 == 4)
            for p, q in pairs:
                if n % 6 == 0:
                    self.assertNotEqual(p % 6, q % 6)
                else:
                    target_mod = 1 if n % 6 == 2 else 5
                    self.assertEqual(p % 6, target_mod)
                    self.assertEqual(q % 6, target_mod)
                self.assertEqual(index_of_prime_gt_three(p) +
                                 index_of_prime_gt_three(q), total)

    def test_sqrt_small_summand_hypothesis_is_false(self):
        """98 has no prime pair whose smaller prime is <= sqrt(98)."""
        n = 98
        smaller_candidates = [p for p in self.primes if p <= math.isqrt(n)]
        self.assertFalse(any(self.is_prime[n - p] for p in smaller_candidates))
        self.assertTrue(self.is_prime[19] and self.is_prime[79])

    def test_coprime_index_witnesses_finite_observation(self):
        """Observed on 10..LIMIT only, not asserted universally."""
        for n in range(10, self.LIMIT + 1, 2):
            t = n // 6 + (n % 6 == 4)
            self.assertTrue(any(
                math.gcd(index_of_prime_gt_three(p), t) == 1
                for p, q in goldbach_pairs_gt_three(n, self.is_prime, self.primes)
            ), f"No coprime-index pair at n={n}")


if __name__ == "__main__":
    unittest.main()
