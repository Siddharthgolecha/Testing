import Mathlib.Tactic
import Mathlib.Data.Nat.Prime.Defs

/-!
# Goldbach: honest proof boundary and a square-root sieve reduction

This is NOT a proof of Goldbach's conjecture. It formalizes exactly what an
elementary divisor-avoidance argument would still have to establish.

* `SurvivesSieve n a` asserts both summands survive all possible divisors
  up to their respective square roots.
* `goldbachAt_iff_exists_sieve` proves that existence of a survivor is
  equivalent to the original Goldbach assertion for this particular `n`.
* `verified_even_cases_through_30` checks 14 explicit even inputs.
No `sorry`, new axioms, or assumed universal witness is used.
-/

namespace Testing.Goldbach

/-- A representation of n as a sum of two primes. -/
def GoldbachAt (n : ℕ) : Prop :=
  ∃ a b : ℕ, Nat.Prime a ∧ Nat.Prime b ∧ a + b = n

/-- Both nontrivial summands escape all possible trial divisors up to sqrt. -/
def SurvivesSieve (n a : ℕ) : Prop :=
  a ≤ n ∧
  2 ≤ a ∧
  2 ≤ n - a ∧
  (∀ d : ℕ, 2 ≤ d → d ≤ Nat.sqrt a → ¬ d ∣ a) ∧
  (∀ d : ℕ, 2 ≤ d → d ≤ Nat.sqrt (n - a) → ¬ d ∣ (n - a))

/-- The square-root sieve conditions are exactly a pair of prime conditions. -/
theorem survivesSieve_iff (n a : ℕ) :
    SurvivesSieve n a ↔
      a ≤ n ∧ Nat.Prime a ∧ Nat.Prime (n - a) := by
  unfold SurvivesSieve
  rw [Nat.prime_def_le_sqrt, Nat.prime_def_le_sqrt]
  tauto

/-- Rigorous reduction: Goldbach at n iff its square-root sieve has a survivor.
    The existential survivor is NOT obtained here for all even n. -/
theorem goldbachAt_iff_exists_sieve (n : ℕ) :
    GoldbachAt n ↔ ∃ a : ℕ, SurvivesSieve n a := by
  constructor
  · rintro ⟨a, b, ha, hb, hsum⟩
    refine ⟨a, (survivesSieve_iff n a).2 ?_⟩
    have hle : a ≤ n := by omega
    have hsub : n - a = b := by omega
    exact ⟨hle, ha, by simpa [hsub] using hb⟩
  · rintro ⟨a, h⟩
    obtain ⟨hle, ha, hb⟩ := (survivesSieve_iff n a).1 h
    exact ⟨a, n - a, ha, hb, by omega⟩

/-- The full open statement: no theorem below claims to establish this. -/
def GoldbachConjecture : Prop :=
  ∀ n : ℕ, 4 ≤ n → Even n → GoldbachAt n

theorem conjecture_iff_sieve_survival :
    GoldbachConjecture ↔
      ∀ n : ℕ, 4 ≤ n → Even n → ∃ a : ℕ, SurvivesSieve n a := by
  simp only [GoldbachConjecture, goldbachAt_iff_exists_sieve]

/-!
### Exactly bounded certification
The following is a finite conjunction, not a claim about all even integers.
Each witness is checked by Lean's prime-number tactic and kernel.
-/

theorem verified_even_cases_through_30 :
    GoldbachAt 4 ∧
    GoldbachAt 6 ∧
    GoldbachAt 8 ∧
    GoldbachAt 10 ∧
    GoldbachAt 12 ∧
    GoldbachAt 14 ∧
    GoldbachAt 16 ∧
    GoldbachAt 18 ∧
    GoldbachAt 20 ∧
    GoldbachAt 22 ∧
    GoldbachAt 24 ∧
    GoldbachAt 26 ∧
    GoldbachAt 28 ∧
    GoldbachAt 30 := by
  constructor
  · exact ⟨2, 2, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 3, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 5, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 7, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨5, 7, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 11, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 13, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨5, 13, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 17, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 19, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨5, 19, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨3, 23, by norm_num, by norm_num, by norm_num⟩
  constructor
  · exact ⟨5, 23, by norm_num, by norm_num, by norm_num⟩
  exact ⟨7, 23, by norm_num, by norm_num, by norm_num⟩

end Testing.Goldbach
