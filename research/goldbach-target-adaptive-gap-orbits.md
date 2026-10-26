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
## Follow-up experiment: exact spatial correlations and gap bounds

For squarefree M, let f(a) be the 0/1 indicator of a and N-a both
being coprime to M. The **two-point correlation** has the exact formula

```text
R_M,N(d) = sum_{a mod M} f(a) f(a+d)
         = product_{p|M} (p - |{0,N,-d,N-d} (mod p)|).
```

To derive this, the four displayed classes are the forbidden values of
a modulo p for the two translated pairs; CRT multiplies allowed counts.
The formula is a standard finite sieve correlation identity, NOT a
claimed new theorem.

Let C_L(u) count valid residues in the L consecutive integers starting
at u, taking u modulo M. Set A=|A_M(N)|, then

```text
T_L := sum_u C_L(u) = L*A
Q_L := sum_u C_L(u)^2
     = L*A + 2*sum_{d=1}^{L-1} (L-d) R_M,N(d).
```

By Cauchy--Schwarz, the number P_L of nonempty length-L windows obeys
P_L >= ceil(T_L^2/Q_L). A maximum cyclic gap G between surviving
residues creates max(0,G-L) empty length-L windows. Therefore, for
1<=L<=M:

```text
G_M(N) <= L + M - ceil((L*A)^2 / Q_L).
```

This is a **rigorous integer bound**, independent of exhaustive wheel
enumeration. All Q_L up to any chosen maximum L can be calculated from
O(L times number_of_wheel_primes) elementary modular operations, using
prefix sums for the correlation terms. It is an application of known
second-moment techniques.

### Results checked against exhaustive enumerations

| M | target N | actual gap | smallest certified bound B | best L |
|---|---:|---:|---:|---:|
| 210 | 212 | 30 | 49 | 30 |
| 210 | 226 | 24 | 42 | 30 |
| 2310 | 2314 | 36 | 146 | 60 |
| 2310 | 2392 | 66 | 188 | 138 |
| 210 | 100 | 24 | 38 | 30 |
| 30030 | 200 | 60 | 460 | 330 |

The M=210, N=100 inequality G<=38 does suffice to prove the *single*
Goldbach instance N=100: the interval [2,98] contains 97 integers, so
contains a wheel survivor, whose two summands must be prime because
every possible prime divisor up to sqrt(100) is included in M.

For N=200, the appropriate square-root-prime wheel is M=30030
(primes 2,3,5,7,11,13). Its global gap is actually 60, but the
second-moment bound 460 exceeds the entire candidate interval
[2,198] (197 integers). **This falsifies the proposed second-moment
certificate as a universal immediate solution**, although it does
not falsify Goldbach.

### Exact finite Fourier transform

Let fhat(h)=sum_{a mod M} f(a)*exp(-2*pi*i*h*a/M). For each p|M
put c_p = h*(M/p)^(-1) mod p. CRT gives

```text
fhat(h) = product_{p|M} (
  p*[c_p=0] - sum_{b in distinct {0,N} mod p}
                   exp(-2*pi*i*c_p*b/p)
).
```

This formula can analyze target-specific phase and correlations,
but rewriting the finite sieve as a Fourier series does not by
itself prove that prime candidates survive inside the required
interval. The accompanying new test suite confirms this factorization
against direct transforms for small moduli.

### Verification and research boundary

Public file: `tests/test_goldbach_correlation_moments.py`.
It checks CRT correlation products, exact squared window counts, Fourier
coefficients, the six quantitative bounds, and Cauchy--Schwarz support
certificates. There are no new Lean claims, no axioms, and no private
research files.

The paired-Jacobsthal work of Ziller--Morack (2017), cited earlier,
already addresses very closely related worst-gap problems.
The present method is a **correct finite bound, not a novelty claim**.
To advance toward universal Goldbach, one needs a substantially
stronger interval-local estimate or provable cancellation beyond
the second-moment/triangle-inequality losses.
