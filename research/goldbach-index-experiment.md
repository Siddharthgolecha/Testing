# Goldbach anti-diagonal experiment: falsifiable index claims

**Status:** exploratory computation only; no new proof and no claim of mathematical novelty.

For a prime \(p>3\), write \(p=6k+s\) with \(s\in\{-1,+1\}\), and \(k\ge1\). For a pair \(p+q=N\) of primes greater than 3:

| Even class | Signs | Index equation |
| --- | --- | --- |
| \(N=6t\) | opposite | \(k+m=t\) |
| \(N=6t+2\) | both + | \(k+m=t\) |
| \(N=6t+4\) | both - | \(k+m=t+1\) |

The four ordered sign combinations reduce to three unordered forms. These are identities, **not** sufficient primality criteria.

## Three examined hypotheses

1. **Baseline finite consistency**: For all even \(10\le N\le 200000\) (99,996 inputs), a prime pair \(p,q>3\) was found; its indices obeyed the relevant equation. This reproduces a vastly weaker finite check than established computational Goldbach verification.
2. **Falsified strengthening:** “Every even \(N\ge10\) admits \(p+q=N\), with \(p\le q\) prime and \(p\le\sqrt N\).” Counterexample: \(N=98\), where the smallest prime summand is \(19\), and \(19>\sqrt{98}\). Indeed \(98=19+79=31+67=37+61\); no prime \(p\le9\) has prime complement. Further examples found were \(122\), \(128\), \(220\), \(63274\). In the finite scan to 200,000 there were 71 even integers \(N\ge10\) with this failure.
3. **Unproved strengthening:** “For every even \(N\ge10\), there is a prime pair \(p,q>3\) whose associated positive indices are coprime, \(\gcd(k,m)=1\).” No counterexample was found among 99,996 inputs \(10\le N\le200000\), but this does **not** imply the statement is true. It is stronger than Goldbach, not an independent sufficient condition for it.

## Index arithmetic

Let \(T=t\) for \(N\equiv0,2\pmod6\) and \(T=t+1\) for \(N\equiv4\pmod6\). Then every qualifying pair satisfies

\[
k+m=T,\qquad\gcd(k,m)=\gcd(k,T).
\]

If \(T\) is prime, \(\gcd(k,m)=1\) holds automatically for any \(1\le k,m<T\). Thus the coprimality observation **does not itself create a route to proving Goldbach**; on those instances it imposes no additional restriction.

## Concrete index witnesses

| N | Prime pair | Signs | Indices (k,m) | Index sum | Smaller prime vs sqrt(N) |
| --- | --- | --- | --- | --- | --- |
| 98 | 19 + 79 | +,+ | (3,13) | 16 | 19 > sqrt(98) |
| 126 | 13 + 113 | +,- | (2,19) | 21 | 13 > sqrt(126) |
| 220 | 23 + 197 | -,- | (4,33) | 37 | 23 > sqrt(220) |
| 63274 | 293 + 62981 | -,- | (49,10497) | 10546 | 293 > sqrt(63274) |

## Reproducibility and proof boundary

The Python unit tests in `tests/test_goldbach_index_experiment.py` check the index identities for **every** prime pair through 20,000, independently falsify the square-root assertion with \(N=98\), and verify the coprime-index observation through 20,000. An additional direct prime-sieve scan was performed through 200,000 to generate the empirical counts reported above. The test code is not Lean and cannot certify any infinite theorem. The Lean work in separate PR #122 concerns only known equivalences and small exact cases.

The next mathematically substantive milestone is a **new theorem that bounds the number of simultaneous complementary-prime exclusions**, rather than extending a finite range or treating a positive local-density heuristic as a proof. Before claiming novelty, compare that theorem with the Hardy–Littlewood singular series and classical sieve theory.
