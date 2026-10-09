import Mathlib.Data.Nat.Basic

/-! # Public Lean toolchain smoke test

Simple theorem to verify the Lean 4 and Mathlib toolchain without copying
private research or assuming unproved results.
-/

namespace Testing

theorem zero_add (n : ℕ) : 0 + n = n := Nat.zero_add n

theorem add_comm (m n : ℕ) : m + n = n + m := Nat.add_comm m n

end Testing
