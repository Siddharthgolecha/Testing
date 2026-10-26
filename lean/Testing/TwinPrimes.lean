import Mathlib.Tactic
import Mathlib.Data.Nat.Prime.Basic

/-!
# Twin prime candidate normal form

This formally proves the classification of twin prime pairs:
apart from (3,5), every pair (p,p+2) of primes has the shape
(6*k-1, 6*k+1) for some k >= 1.

The converse says **only** that when both generated numbers are prime,
they are twin primes. This module does not claim to prove that infinitely
many such indices exist.

It also proves an infinite family of k for which both candidates are
composite, showing the shape itself never guarantees primality.
No new axioms or `sorry`.
-/

namespace Testing.TwinPrimes

def IsTwinIndex (k : ℕ) : Prop :=
  Nat.Prime (6 * k - 1) ∧ Nat.Prime (6 * k + 1)

/-- Every twin-prime pair beyond (3,5) has the 6k-1, 6k+1 form. -/
theorem twin_prime_normal_form (p : ℕ)
    (hp : Nat.Prime p) (hq : Nat.Prime (p + 2)) (hlarge : 3 < p) :
    ∃ k : ℕ, 1 ≤ k ∧ p = 6 * k - 1 ∧ p + 2 = 6 * k + 1 := by
  have hodd : p % 2 = 1 := by
    rcases hp.eq_two_or_odd with h2 | hodd
    · omega
    · exact hodd
  have hnot3 : p % 3 ≠ 0 := by
    intro hz
    have hdvd : 3 ∣ p := Nat.dvd_of_mod_eq_zero hz
    have heq : p = 3 := (hp.dvd_iff_eq (by decide)).mp hdvd
    omega
  have hqnot3 : (p + 2) % 3 ≠ 0 := by
    intro hz
    have hdvd : 3 ∣ p + 2 := Nat.dvd_of_mod_eq_zero hz
    have heq : p + 2 = 3 := (hq.dvd_iff_eq (by decide)).mp hdvd
    omega
  have hmod : p % 6 = 5 := by omega
  refine ⟨(p + 1) / 6, ?_, ?_, ?_⟩ <;> omega

/-- Candidate primality is equivalent to the corresponding pair being twin primes. -/
theorem twin_index_iff (k : ℕ) (hk : 1 ≤ k) :
    IsTwinIndex k ↔
      ∃ p : ℕ, Nat.Prime p ∧ Nat.Prime (p + 2) ∧ p = 6 * k - 1 := by
  constructor
  · rintro ⟨hp, hq⟩
    refine ⟨6 * k - 1, hp, ?_, rfl⟩
    have h : (6 * k - 1) + 2 = 6 * k + 1 := by omega
    simpa only [h] using hq
  · rintro ⟨p, hp, hq, rfl⟩
    refine ⟨hp, ?_⟩
    have h : (6 * k - 1) + 2 = 6 * k + 1 := by omega
    simpa only [h] using hq

/-- A concrete candidate pair in which both numbers are composite. -/
theorem both_composite_at_20 :
    ¬Nat.Prime (6 * 20 - 1) ∧ ¬Nat.Prime (6 * 20 + 1) := by
  norm_num [Nat.prime_def_le_sqrt]

/-- Infinitely many candidate indices have both entries composite.
Here, k = 35*t + 1 with t >= 1, and 6*k±1 factor through 5 and 7. -/
theorem both_composite_family (t : ℕ) (ht : 1 ≤ t) :
    ¬Nat.Prime (6 * (35 * t + 1) - 1) ∧
    ¬Nat.Prime (6 * (35 * t + 1) + 1) := by
  have hm : 6 * (35 * t + 1) - 1 = 5 * (42 * t + 1) := by omega
  have hp : 6 * (35 * t + 1) + 1 = 7 * (30 * t + 1) := by omega
  constructor
  · rw [hm]
    exact Nat.not_prime_mul (by decide) (by omega)
  · rw [hp]
    exact Nat.not_prime_mul (by decide) (by omega)

end Testing.TwinPrimes
