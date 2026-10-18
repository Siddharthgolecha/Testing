import Mathlib.Tactic

/-!
# Parametric all-reply rank induction for a memoryless controller

A completed controller round is a single directed edge: it fixes White's
selected action and allows *every* legal Black reply.  This lemma never
replaces the selected action with a searched winning action.

The independent KRK obligation is to construct a global rank whose value
strictly decreases on every such edge.  This file proves the induction
principle only; it is **not** a proof of that geometric obligation.
-/

namespace Testing.GeometricController

/-- Finite-horizon, all-reply success for an abstract completed-round graph. -/
def AllReplyWinsWithin {State : Type} (step : State → State → Prop)
    (mate : State → Prop) : Nat → State → Prop
  | 0, s => mate s
  | k + 1, s =>
      mate s ∨ ((∃ t, step s t) ∧
        ∀ t, step s t → AllReplyWinsWithin step mate k t)

/-- Extra fuel cannot invalidate a certificate. -/
theorem allReplyWinsWithin_mono {State : Type}
    {step : State → State → Prop} {mate : State → Prop}
    (k l : Nat) (hkl : k ≤ l) (s : State)
    (h : AllReplyWinsWithin step mate k s) :
    AllReplyWinsWithin step mate l s := by
  induction l generalizing k s with
  | zero =>
      have hk : k = 0 := by omega
      subst k
      exact h
  | succ l ih =>
      cases k with
      | zero =>
          exact Or.inl h
      | succ k =>
          change mate s ∨
            ((∃ t, step s t) ∧
              ∀ t, step s t → AllReplyWinsWithin step mate k t) at h
          change mate s ∨
            ((∃ t, step s t) ∧
              ∀ t, step s t → AllReplyWinsWithin step mate l t)
          rcases h with hm | ⟨hex, hall⟩
          · exact Or.inl hm
          · exact Or.inr ⟨hex, fun t ht => ih k (by omega) t (hall t ht)⟩

/-- One-shot termination of the *fixed* all-reply transition relation from
a global well-founded numerical rank.  The rank-zero and successor clauses
are independently verifiable geometry obligations; neither is assumed to be
true of KRK here. -/
theorem allReplyWinsWithin_of_strict_rank {State : Type}
    (step : State → State → Prop) (mate : State → Prop)
    (rank : State → Nat)
    (hzero : ∀ s, rank s = 0 → mate s)
    (hprogress : ∀ s, 0 < rank s → ∃ t, step s t)
    (hdecrease : ∀ s t, step s t → rank t < rank s) :
    ∀ s, AllReplyWinsWithin step mate (rank s) s := by
  have hinduct : ∀ k : Nat, ∀ s, rank s = k →
      AllReplyWinsWithin step mate k s := by
    intro k
    induction k using Nat.strong_induction_on with
    | h k ih =>
        intro s hs
        cases k with
        | zero =>
            change mate s
            exact hzero s (by simpa [hs])
        | succ j =>
            change mate s ∨
              ((∃ t, step s t) ∧
                ∀ t, step s t → AllReplyWinsWithin step mate j t)
            right
            constructor
            · exact hprogress s (by omega)
            · intro t ht
              have hlt : rank t < j + 1 := by
                have hstrict := hdecrease s t ht
                omega
              have hcert := ih (rank t) hlt t rfl
              exact allReplyWinsWithin_mono (rank t) j (by omega) t hcert
  intro s
  exact hinduct (rank s) s rfl

end Testing.GeometricController
