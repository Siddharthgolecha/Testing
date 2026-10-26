"""Exact target-dependent pair-sieve correlations and honest gap certificates.

The mathematics is a finite CRT/second-moment identity; it is *not* a
new proof of Goldbach, nor claimed to be a novel number-theoretic theorem.
Only standard-library modules are used, so CI remains independent of Qiskit.
"""

import cmath
import math
import unittest


def prime_divisors_squarefree(modulus):
    """Factor a squarefree positive modulus into its distinct prime factors."""
    n = modulus
    factors = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            n //= p
            if n % p == 0:
                raise ValueError("modulus must be squarefree")
        p += 1
    if n > 1:
        factors.append(n)
    return tuple(factors)


def candidate_mask(modulus, target):
    return tuple(
        int(math.gcd(a, modulus) == 1 and math.gcd(target - a, modulus) == 1)
        for a in range(modulus)
    )


def crt_survivor_count(primes, target):
    return math.prod(p - (1 if target % p == 0 else 2) for p in primes)


def crt_pair_correlation(primes, target, separation):
    """R(d) = #a for which a,a+d, N-a,N-a-d are wheel-coprime."""
    return math.prod(
        p - len({0, target % p, (-separation) % p,
                 (target - separation) % p})
        for p in primes
    )


def circular_window_counts(mask, length):
    """Number of survivors in each length-L cyclic integer window."""
    modulus = len(mask)
    assert 1 <= length <= modulus
    doubled = mask + mask[:length-1]
    partial = [0]
    for x in doubled:
        partial.append(partial[-1] + x)
    return tuple(partial[a+length] - partial[a] for a in range(modulus))


def analytic_window_energy(modulus, target, length):
    """Exact sum of squared window counts without enumerating the wheel."""
    factors = prime_divisors_squarefree(modulus)
    a = crt_survivor_count(factors, target)
    q = length * a
    q += 2 * sum(
        (length - d) * crt_pair_correlation(factors, target, d)
        for d in range(1, length)
    )
    return a, q


def moment_gap_bound(modulus, target, max_length):
    """Certified upper bound on maximum cyclic gap.

    Let T=L*A and Q=sum_start C(start)^2. Cauchy--Schwarz gives
    #nonempty windows >= ceil(T*T/Q). A cyclic gap of G between
    survivors creates max(0,G-L) empty windows. Hence:
    G <= L + M - ceil(T*T/Q).
    """
    if not 1 <= max_length <= modulus:
        raise ValueError("window lengths must be 1..modulus")
    primes = prime_divisors_squarefree(modulus)
    a = crt_survivor_count(primes, target)
    if not a:
        raise ValueError("no admissible residues")
    q = 0
    prefix_r = 0
    best = None
    for length in range(1, max_length + 1):
        if length > 1:
            prefix_r += crt_pair_correlation(primes, target, length - 1)
        q += a + 2 * prefix_r
        t = length * a
        positive_windows_at_least = (t*t + q - 1) // q
        bound = length + modulus - positive_windows_at_least
        candidate = (bound, length, positive_windows_at_least)
        if best is None or candidate[0] < best[0]:
            best = candidate
    return best


def max_cyclic_gap(mask):
    survivors = [a for a, is_valid in enumerate(mask) if is_valid]
    if not survivors:
        raise ValueError("no survivors")
    return max(
        right - left
        for left, right in zip(
            survivors, survivors[1:] + [survivors[0] + len(mask)]
        )
    )


def local_fourier_coefficient(modulus, target, frequency):
    """CRT factorization of the discrete Fourier transform of the mask."""
    factors = prime_divisors_squarefree(modulus)
    coeff = 1 + 0j
    for p in factors:
        other = modulus // p
        c = frequency * pow(other, -1, p) % p
        forbidden = {0, target % p}
        local = (p if c == 0 else 0) - sum(
            cmath.exp(-2j * math.pi * c * b / p) for b in forbidden
        )
        coeff *= local
    return coeff


class TestGoldbachCorrelationMoments(unittest.TestCase):
    def test_crt_correlations_and_energies_match_direct_enumeration(self):
        for modulus in (30, 210):
            factors = prime_divisors_squarefree(modulus)
            for target in range(0, modulus, 2):
                mask = candidate_mask(modulus, target)
                self.assertEqual(sum(mask), crt_survivor_count(factors, target))
                for d in (0, 1, 2, 3, 5, 7, 11):
                    direct = sum(mask[a] * mask[(a+d) % modulus]
                                 for a in range(modulus))
                    self.assertEqual(
                        direct, crt_pair_correlation(factors, target, d)
                    )
                for length in (1, 2, 5, 10, 20):
                    counts = circular_window_counts(mask, length)
                    a, q = analytic_window_energy(modulus, target, length)
                    self.assertEqual(sum(counts), length * a)
                    self.assertEqual(sum(c*c for c in counts), q)

    def test_crt_fourier_factorization(self):
        for modulus, targets, frequencies in (
            (30, (14, 16), tuple(range(30))),
            (210, (212, 226), (0, 1, 2, 5, 13, 17, 105)),
        ):
            for target in targets:
                mask = candidate_mask(modulus, target)
                for h in frequencies:
                    direct = sum(
                        v * cmath.exp(-2j * math.pi * h * a / modulus)
                        for a, v in enumerate(mask) if v
                    )
                    derived = local_fourier_coefficient(modulus, target, h)
                    self.assertAlmostEqual(direct.real, derived.real, places=8)
                    self.assertAlmostEqual(direct.imag, derived.imag, places=8)

    def test_absolute_fourier_certificate_is_weaker(self):
        """L1 over Fourier modes loses more phase cancellation than moments.

        If the h!=0 coefficient bound is smaller than the mean,
        *every* length-L cyclic window must be nonempty.
        """
        for modulus, target, predicted_first in (
            (210, 212, 72),
            (210, 226, 60),
        ):
            # Exact CRT-local Fourier coefficients; not an FFT approximation.
            factors = prime_divisors_squarefree(modulus)
            a = crt_survivor_count(factors, target)
            coeffs = [
                abs(local_fourier_coefficient(modulus, target, h))
                for h in range(1, modulus)
            ]
            first_certified = None
            for length in range(1, modulus + 1):
                error_bound = sum(
                    amp * abs(math.sin(math.pi * h * length / modulus)
                              / math.sin(math.pi * h / modulus))
                    for h, amp in enumerate(coeffs, start=1)
                ) / modulus
                mean = length * a / modulus
                if mean > error_bound + 1e-8:
                    first_certified = length
                    break
            self.assertEqual(first_certified, predicted_first)
            self.assertLess(
                moment_gap_bound(modulus, target, 200)[0], first_certified
            )

    def test_max_gap_certificates_and_weakness(self):
        for modulus, target, max_length, expected_bound, expected_L, actual in (
            (210, 212, 200, 49, 30, 30),
            (210, 226, 200, 42, 30, 24),
            (2310, 2314, 200, 146, 60, 36),
            (2310, 2392, 200, 188, 138, 66),
            (210, 100, 200, 38, 30, 24),
            (30030, 200, 500, 460, 330, 60),
        ):
            bound, chosen_L, nonempty_at_least = moment_gap_bound(
                modulus, target, max_length
            )
            self.assertEqual((bound, chosen_L), (expected_bound, expected_L))
            self.assertGreater(nonempty_at_least, 0)
            mask = candidate_mask(modulus, target)
            self.assertEqual(max_cyclic_gap(mask), actual)
            self.assertLessEqual(actual, bound)
        # M=210 includes every prime <= sqrt(100); the worst-gap
        # certificate below the interval size can certify N=100.
        self.assertLess(moment_gap_bound(210, 100, 200)[0], 100 - 3)
        # M=30030 includes every prime <= sqrt(200), but the
        # moment bound is too weak to certify N=200 by worst gaps.
        self.assertGreater(moment_gap_bound(30030, 200, 500)[0], 200 - 3)

    def test_short_range_correlations_do_not_determine_longest_gap(self):
        """Two targets agree on R(d), 0<=d<=11, but have distinct gaps."""
        modulus = 2310
        n1, n2 = 38, 82
        primes = prime_divisors_squarefree(modulus)
        self.assertEqual(crt_survivor_count(primes, n1), 135)
        self.assertEqual(crt_survivor_count(primes, n2), 135)
        for d in range(12):
            self.assertEqual(
                crt_pair_correlation(primes, n1, d),
                crt_pair_correlation(primes, n2, d),
                f"first differing separation should be 12, not {d}",
            )
        self.assertNotEqual(
            crt_pair_correlation(primes, n1, 12),
            crt_pair_correlation(primes, n2, 12),
        )
        self.assertEqual(max_cyclic_gap(candidate_mask(modulus, n1)), 42)
        self.assertEqual(max_cyclic_gap(candidate_mask(modulus, n2)), 66)

    def test_nonempty_window_cauchy_schwarz_certificate(self):
        for modulus, target, length in (
            (210, 212, 30), (210, 226, 30),
            (2310, 2314, 60), (2310, 2392, 138),
        ):
            mask = candidate_mask(modulus, target)
            counts = circular_window_counts(mask, length)
            a, q = analytic_window_energy(modulus, target, length)
            min_positive = ((length*a)**2 + q - 1) // q
            self.assertGreaterEqual(sum(c > 0 for c in counts), min_positive)


if __name__ == "__main__":
    unittest.main()
