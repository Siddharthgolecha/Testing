"""Goldbach target-centered Fourier phases: exact finite diagnostics.

No new Goldbach theorem is asserted. Numpy is included through the pinned
Qiskit test environment, but the target-centered formula is finite math.
"""

import math
import unittest

import numpy as np


def centered_spectral_diagnostics(modulus, target):
    """Return C, its average term, signed correction, and naive L1 error.

    For even N, the cyclic pair mask satisfies f(N-a) = f(a).
    Hence exp(pi*i*h*N/M) * FFT(f)[h] is real. For the symmetric
    finite interval [2,N-2], the Fourier window kernel is the
    real Dirichlet factor sin(pi*h*(N-3)/M)/sin(pi*h/M).
    """
    assert target >= 4 and target % 2 == 0
    a = np.arange(modulus, dtype=np.int64)
    mask = ((np.gcd(a, modulus) == 1) &
            (np.gcd(target - a, modulus) == 1)).astype(np.int64)
    spectrum = np.fft.fft(mask)
    h = np.arange(1, modulus)
    midpoint_phase = np.exp(1j * np.pi * h * target / modulus)
    centered = midpoint_phase * spectrum[1:]
    length = target - 3
    kernel = (np.sin(np.pi * h * length / modulus) /
              np.sin(np.pi * h / modulus))
    average = length * int(mask.sum()) / modulus
    signed = float(np.sum(centered.real * kernel) / modulus)
    naive = float(np.sum(np.abs(spectrum[1:]) * np.abs(kernel)) / modulus)
    direct = sum(
        int(mask[a % modulus]) for a in range(2, target - 1)
    )
    return direct, average, signed, naive, float(np.max(np.abs(centered.imag)))


class TestGoldbachCenteredFourier(unittest.TestCase):
    def test_centered_formula_reconstructs_finite_interval(self):
        for modulus, target, expected_count in (
            (210, 100, 10),
            (30030, 200, 12),
        ):
            direct, average, signed, naive, imaginary_error = (
                centered_spectral_diagnostics(modulus, target)
            )
            self.assertEqual(direct, expected_count)
            self.assertAlmostEqual(average + signed, direct, places=7)
            self.assertLess(imaginary_error, 1e-7)
            self.assertLessEqual(abs(signed), naive + 1e-8)

    def test_naive_spectral_certificate_fails_at_200(self):
        _, mu100, correction100, error100, _ = (
            centered_spectral_diagnostics(210, 100)
        )
        _, mu200, correction200, error200, _ = (
            centered_spectral_diagnostics(30030, 200)
        )
        self.assertAlmostEqual(correction100, 0.761904761904762, places=7)
        self.assertLess(error100, mu100)
        self.assertAlmostEqual(correction200, -0.989010989010989, places=6)
        self.assertGreater(error200, mu200)
        self.assertGreater(error200, 20 * abs(correction200))


if __name__ == "__main__":
    unittest.main()
