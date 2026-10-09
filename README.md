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
