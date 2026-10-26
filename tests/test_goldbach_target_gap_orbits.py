"""Target-adaptive Goldbach wheel: phase versus local density.

Public, finite falsification experiment. No assertion of Goldbach or novelty.
Compatible with the Testing repository's standard unittest discovery.
"""

import math
import unittest


def wheel_survivors(modulus, target):
    """All residues a mod M with gcd(a,M)=gcd(target-a,M)=1."""
    return tuple(
        a for a in range(modulus)
        if math.gcd(a, modulus) == 1
        and math.gcd(target - a, modulus) == 1
    )


def cyclic_gaps(modulus, survivors):
    assert survivors
    return tuple(
        right - left
        for left, right in zip(
            survivors, survivors[1:] + (survivors[0] + modulus,)
        )
    )


def predicted_count(primes, target):
    """Squarefree CRT local factor: one or two forbidden classes per p."""
    return math.prod(p - 1 if target % p == 0 else p - 2 for p in primes)


class TestTargetAdaptiveGoldbachWheel(unittest.TestCase):
    def test_complete_local_count_for_210(self):
        primes = (2, 3, 5, 7)
        modulus = math.prod(primes)
        for target in range(0, modulus, 2):
            survivors = wheel_survivors(modulus, target)
            self.assertEqual(len(survivors), predicted_count(primes, target))
            # Involution a -> target - a preserves the admissible set.
            self.assertEqual(
                {((target - a) % modulus) for a in survivors},
                set(survivors),
            )
            self.assertEqual(sum(cyclic_gaps(modulus, survivors)), modulus)

    def test_same_density_but_different_gap_at_210(self):
        modulus = 210
        n1, n2 = 212, 226
        a = wheel_survivors(modulus, n1)
        b = wheel_survivors(modulus, n2)
        self.assertEqual(math.gcd(n1, modulus), math.gcd(n2, modulus))
        self.assertEqual((len(a), len(b)), (15, 15))
        self.assertEqual((max(cyclic_gaps(modulus, a)),
                          max(cyclic_gaps(modulus, b))), (30, 24))
        # Multiplication by a unit permutes the candidates.
        unit = 113
        self.assertEqual(math.gcd(unit, modulus), 1)
        self.assertEqual((unit * n1) % modulus, n2 % modulus)
        self.assertEqual({(unit * x) % modulus for x in a}, set(b))

    def test_stronger_same_density_different_gap_at_2310(self):
        modulus = 2310
        primes = (2, 3, 5, 7, 11)
        n1, n2 = 2314, 2392
        a = wheel_survivors(modulus, n1)
        b = wheel_survivors(modulus, n2)
        self.assertEqual(math.gcd(n1, modulus), 2)
        self.assertEqual(math.gcd(n2, modulus), 2)
        self.assertEqual(predicted_count(primes, n1), 135)
        self.assertEqual(predicted_count(primes, n2), 135)
        self.assertEqual((len(a), len(b)), (135, 135))
        self.assertEqual((max(cyclic_gaps(modulus, a)),
                          max(cyclic_gaps(modulus, b))), (36, 66))
        self.assertIn(1163, b)
        self.assertIn(1229, b)
        self.assertEqual(1229 - 1163, 66)
        self.assertFalse(any(1163 < x < 1229 for x in b))
        unit = 1753
        self.assertEqual(math.gcd(unit, modulus), 1)
        self.assertEqual((unit * n1) % modulus, n2 % modulus)
        self.assertEqual({(unit * x) % modulus for x in a}, set(b))

    def test_admissible_wheel_pair_need_not_be_prime_pair(self):
        modulus = 2310
        target = 338
        half = 169  # 13*13, but 13 is not among factors of 2310
        self.assertIn(half, wheel_survivors(modulus, target))
        self.assertEqual(13 * 13, half)
        self.assertEqual(half + half, target)

    def test_target_periodicity(self):
        for modulus in (30, 210):
            for target in (12, 98, 226):
                self.assertEqual(
                    wheel_survivors(modulus, target),
                    wheel_survivors(modulus, target + modulus),
                )


if __name__ == "__main__":
    unittest.main()
