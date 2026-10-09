# Testing — public Qiskit + Lean CI sandbox

This repository provides **independent, reproducible smoke tests** for Qiskit (Python) and Lean 4 + Mathlib via GitHub Actions. It does not contain or checkout the private `coalescent-research` repository.

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
4. Open **Actions → Private Coalescent CI (ephemeral) → Run workflow**, select the private branch/tag/commit to test (default `research/schi-next-reversible-step`), then select **`schi-next`**, **`lean-smoke`**, or **`both`**.

The workflow exists but **cannot access the private repository until the key is installed**. Its existing public workflow is not evidence that this private checkout has passed. Use a dedicated read-only key; revoke it from **Deploy keys** and delete the `Testing` secret when it is no longer needed.

### Security and reproducibility boundaries

- This private-code workflow is **manual-dispatch only**; it does not run on public PRs, forks, or pushes. `GITHUB_TOKEN` is read-only, SSH checkout uses `persist-credentials: false`, and neither uploaded artifacts nor public caches contain research files. The private source is erased from the working directory in an `always()` cleanup step, and the hosted runner is ephemeral.
- Private Python/Lean build output is redirected to temporary runner files. Public logs show only **PASS/FAIL**, not source lines or tracebacks; a failure therefore requires private/local diagnosis. Checkout and setup actions can still expose non-source metadata, and a compromised workflow/action or arbitrary code under test can intentionally disclose private source. **Do not treat this as a security isolation guarantee.**
- The **selected private ref appears in public workflow dispatch metadata**, so use an appropriate commit identifier if you do not want a descriptive branch name visible.
- The `schi-next` suite installs Testing's pinned public Qiskit dependencies and runs the checked-out private repository's `chess/experiments/schi_next/test_*.py` tests. It does **not** by itself establish Qiskit native transpilation or quantum hardware correctness.
- The `lean-smoke` suite compiles `RecordAlgebra.Kernel.FiniteModel` inside the private repository's `lean-proofs` package, with GitHub caching of private Lean build outputs disabled. It does not compile every Lean theorem in the repository.
- Do not give write access to the deploy key, expose credentials to fork workflows, or enable public log/artifact uploads for private tests. Restrict write access to this public repository: anyone who can modify a credential-bearing workflow may be able to misuse its secret.
