# Testing — public Qiskit + Lean CI sandbox

This repository provides **independent, reproducible smoke tests** for Qiskit (Python) and Lean 4 + Mathlib via GitHub Actions. The default smoke workflow never checks out private code. A **separate, manually dispatched** workflow can temporarily checkout `coalescent-research` on an ephemeral runner with a dedicated read-only SSH deploy key, without committing it here.

## Toolchains

- **Qiskit:** Python 3.11, Qiskit 2.2.3, Qiskit Aer 0.17.2, and `unittest` (pinned in `requirements.txt`).
- **Lean:** Lean 4.32.1 and Mathlib 4.32.1 (aligned with the Lean toolchain of `coalescent-research`), managed by `elan`/`lake`. Transitive Mathlib dependencies are pinned by `lean/lake-manifest.json`.
- **CI:** `.github/workflows/toolchain-ci.yml` runs two separate jobs on standard `ubuntu-latest` GitHub-hosted runners for each push and pull request, and supports manual `workflow_dispatch`.

## Run tests

### Python/Qiskit

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p 'test_*.py' -v
```

### Lean

Install [elan](https://github.com/leanprover/elan), then from the repository root:

```bash
cd lean
lake build Testing.Smoke
```

On GitHub, use **Actions → Toolchain CI → Run workflow** or push a branch/open a PR. The CI logs report the actual installed versions. The Mathlib download/cache may take longer on the first run.

## Adding experiments

Put public, shareable Qiskit tests in `tests/`, and Lean modules in `lean/Testing/`; update the workflow to build new Lean targets. For expensive experiments use a separately reviewed workflow and explicit resource caps.

**Public-repository warning:** do not commit or print private source code, unreleased research results, API tokens, keys, credentials, non-public data or artifacts from `coalescent-research`. Actions logs and uploaded artifacts are public. No private-repository checkout, PAT, or other secret is required for these smoke tests.

Standard GitHub-hosted runners are free on public repositories; GitHub still has usage/concurrency limits, and larger runners or excess artifact/cache storage can be billable.

## Ephemeral private Coalescent CI (manual only)

The separate [Private Coalescent CI (ephemeral)](.github/workflows/private-coalescent-ci.yml) workflow can **temporarily** check out `Siddharthgolecha/coalescent-research` on an isolated GitHub-hosted runner, execute selected tests, and discard the checkout. The original public Qiskit/Lean smoke workflow stays independent. **No research files or commits are added to this public repository.** This is not a way to make private source inaccessible to a compromised runner or to someone who can edit privileged workflows.

### One-time read-only credential setup

1. Generate a dedicated SSH keypair **on your own machine**, for example `ssh-keygen -t ed25519 -C 'Testing read-only CI' -f ./coalescent-testing-deploy -N ''`. **Never commit either key.**
2. In the **private** `coalescent-research` repository, open **Settings → Deploy keys → Add deploy key**. Paste the contents of `coalescent-testing-deploy.pub` and **leave “Allow write access” unchecked**.
3. In the **public** `Testing` repository, open **Settings → Secrets and variables → Actions → New repository secret**. Name it `COALESCENT_DEPLOY_KEY` and paste the **private** key's complete multiline contents from `coalescent-testing-deploy`. Do not paste it into chat, a workflow file, or an issue.
4. Open **Actions → Private Coalescent CI (ephemeral) → Run workflow**, select the private branch/tag/commit to test (default `research/schi-next-reversible-step`), then select **`schi-next`**, **`lean-smoke`**, **`both`**, **`theory-krk`**, or **`theory-lean`**.

The workflow exists but **cannot access the private repository until the key is installed**. Its existing public workflow is not evidence that this private checkout has passed. Use a dedicated read-only key; revoke it from **Deploy keys** and delete the `Testing` secret when it is no longer needed.

### Security and reproducibility boundaries

- This private-code workflow is **manual-dispatch only**; it does not run on public PRs, forks, or pushes. `GITHUB_TOKEN` is read-only, SSH checkout uses `persist-credentials: false`, and neither uploaded artifacts nor public caches contain research files. The private source is erased from the working directory in an `always()` cleanup step, and the hosted runner is ephemeral.
- Private Python/Lean build output is redirected to temporary runner files. Public logs show only **PASS/FAIL**, not source lines or tracebacks; a failure therefore requires private/local diagnosis. Checkout and setup actions can still expose non-source metadata, and a compromised workflow/action or arbitrary code under test can intentionally disclose private source. **Do not treat this as a security isolation guarantee.**
- The **selected private ref appears in public workflow dispatch metadata**, so use an appropriate commit identifier if you do not want a descriptive branch name visible.
- The `schi-next` suite installs Testing's pinned public Qiskit dependencies and runs the checked-out private repository's `chess/experiments/schi_next/test_*.py` tests. It does **not** by itself establish Qiskit native transpilation or quantum hardware correctness.
- The `lean-smoke` suite compiles `RecordAlgebra.Kernel.FiniteModel` inside the private repository's `lean-proofs` package, with GitHub caching of private Lean build outputs disabled. It does not compile every Lean theorem in the repository.
- Do not give write access to the deploy key, expose credentials to fork workflows, or enable public log/artifact uploads for private tests. Restrict write access to this public repository: anyone who can modify a credential-bearing workflow may be able to misuse its secret.

### KRK theory validation (2026-10-09)

The **manual-only** `theory-krk` suite uses the same read-only deploy key to fetch the selected private ref, plus a second runner-local checkout of private `main` solely for the merged canonical KRK-v1 `reference.py` and `api.py` rules. Those canonical sources are copied **inside the ephemeral runner** for cross-contract tests; neither checkout is committed, cached or uploaded. It runs an allowlist of private 4×4 geometry, D4 equivariance, rank and direct canonical integration tests, then compiles the private 155-wire directional-step gate list to Qiskit (164 wires after clean MCX lowering), invokes `transpile` to an ideal `x/sx/rz/cx` basis, and runs a bounded Aer matrix-product-state basis fixture. Public logs show only PASS/FAIL, not private source, test names, tracebacks, gate statistics or input states.

The separate **manual-only** `theory-lean` suite checks four private `RecordAlgebra/QuantumChess` theorem files using `lake env lean` in `lean-proofs`, and rejects literal proof-hole and axiom declarations. It proves only what those files actually contain: passing does not establish complete KRK semantics or a quantum advantage. `schi-next`, `lean-smoke`, and `both` keep their previous behavior.

To test the draft theory work, choose **Actions → Private Coalescent CI (ephemeral) → Run workflow**, set `source_ref` to `theory/coalescent-history-foundations` (or a pinned full SHA), and choose `theory-krk` or `theory-lean`. The current GitHub connector cannot issue a workflow dispatch itself; changes to this workflow do **not** count as successful private CI execution. A human must click **Run workflow**. Since this repository is public, branch names and commit identifiers used in dispatch inputs can remain visible in public metadata.


### Hamiltonian PR #206 and mathematical PR #207 validation (2026-10-10)

Two additional options were added to the **existing manual-only ephemeral**
workflow; there are no private repository source files in this public
Testing repository, and no public push-trigger for private code.

Use **Actions → Private Coalescent CI (ephemeral) → Run workflow**.

- To verify the coherent Hamiltonian and symmetry-optimal-move circuit
  from private PR #206, supply its **exact head commit SHA** as
  `source_ref` and select `hamiltonian-206`. The allowlist runs ten
  private Qiskit/Aer, canonical legality, history, spectrum and phase
  interference suites. A test failure stops the run with only a
  public-safe suite-name/FAIL status.
- To verify the mathematical strategy results from private PR #207,
  supply its **exact head SHA** as `source_ref` and select
  `hamiltonian-207`. It runs the independent game-theory,
  seven-round-policy, exact geometric-rank formula, and symbolic-rank
  regression suites against the private canonical KRK semantics.

The human-triggered workflow is still the **only** testing action
supported here. Merely adding a suite or committing its test files
is **not** evidence of a passing Qiskit run. Its read-only deploy key,
private log suppression, runner-local checkout and `always()`
cleanup remain unchanged. Pin the commit SHA, because the research
branches are still advancing. If an allowlisted private test fails,
diagnose it in a private runner or local checkout rather than
printing private tracebacks into this public repository.
