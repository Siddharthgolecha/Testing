# Target-adaptive Goldbach wheel: a phase-sensitive obstruction

**Research status:** exact finite computations and standard CRT deductions only. No new universal Goldbach theorem, no novelty claim.

## Motivation

Given a squarefree wheel M (here M = 30, 210, 2310), define

A_M(N) = {a in {0,...,M-1}: gcd(a,M)=gcd(N-a,M)=1}.

It is symmetric under the reflection a -> N-a (mod M). The count is the familiar local factor product

|A_M(N)| = product_{p | M} [p-1 if p | N, else p-2].

Its density depends on which wheel primes divide N, but not on the finer value of N modulo M.

## A target-phase theorem (CRT, not new)

For squarefree M, if gcd(N1,M)=gcd(N2,M), there exists a unit u modulo M such that u*N1 = N2 (mod M). This follows by choosing u=1 at primes dividing both targets, and u=N2/N1 at all other prime moduli, then using CRT.

Multiplication by this u maps A_M(N1) bijectively to A_M(N2), because both members of the pair scale by the same unit.

**But the multiplication generally does not preserve adjacency / ordinary numerical distances around the circle of residues.** Therefore identical local densities do not imply identical or monotonically ordered longest survivor gaps.

## Exact counterexamples to density-determines-gap

Define G_M(N) as the largest cyclic difference between successive sorted elements of A_M(N).

| M | N1 | N2 | gcd(Ni,M) | |A_M(Ni)| | G_M(N1) | G_M(N2) | unit u mapping 1 -> 2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 210 | 212 | 226 | 2 | 15 | 30 | 24 | 113 |
| 2310 | 2314 | 2392 | 2 | 135 | 36 | 66 | 1753 |

For M=2310, N2=2392, the admissible residue 1163 is followed by 1229, with no admissible residue between: a 66-step gap. Yet N1 has the same predicted density and a maximum gap of 36.

Also, with M=210, N=216 has **twice the residue count** (30 rather than 15 at N=226), but its maximal cyclic gap is **larger** (28 rather than 24). Thus even higher survivor density need not entail smaller maximal gaps.

These are straightforward finite, checkable observations rather than new number-theoretic breakthroughs.

## Why even phase-sensitive wheel counts are not Goldbach

A positive local density describes a periodic set of residues, not the existence of a surviving integer in the finite interval [2,N-2]. Moreover, survivors need not be prime. For M=2310 and N=338, a=N-a=169=13^2 survives because gcd(169,2310)=1, but both summands are composite.

## What the literature already covers

- Ziller & Morack (2017), *Divisibility in paired progressions, Goldbach's conjecture, and the infinitude of prime pairs*, https://arxiv.org/abs/1706.00317, define a generalized Jacobsthal function for paired progressions and derive conditional implications for Goldbach and twin primes.
- Ziller & Morack (2017), *A short note on the computation of the generalised Jacobsthal function for paired progressions*, https://arxiv.org/abs/1706.03668, compute its values for primorials to 73.
- OEIS A288815: https://oeis.org/A288815.

We do **not** rebrand a paired-Jacobsthal gap bound as a new conjecture. The useful lesson from this experiment is that a target-specific proof technique must track positional/phase information beyond the singular-series/local-count factors.

## Reproducibility

Run the public self-contained Python test:

```bash
python -m unittest tests/test_goldbach_target_gap_orbits.py -v
```

The suite exhaustively checks the exact count formula and reflection symmetry for all even N mod 210, verifies both targeted M=2310 cases with explicit unit maps and gap witnesses, and checks a composite survivor. No private data. These are computational checks, not Lean-certified infinite claims.

## Research go/no-go criterion

Before proposing a new phase-discrepancy theorem, compare it quantitatively with the generalized Jacobsthal results and classical sieve / Fourier methods. The target should be a *new quantitative bound* on local survivor placement in an interval of length relevant to N, not a restatement of existence or periodicity.