---
name: cpv-publish-pipeline-canon
description: "how does webdesign publish / why is the release pipeline set up this way / RC-PIPELINE-DRIFT-001 / why is CPV pinned to a version / where do SBOM + attestation + SHA256SUMS come from / green CI but cross-refs did not run"
ocd: 2026-07-13
lmd: 2026-07-13
metadata:
  node_type: memory
  type: project
  tier: component
  globs: ["scripts/publish.py", ".github/workflows/**", ".jscpd.json"]
---

webdesign publishes ONLY through `scripts/publish.py` — never a bare `git push` (a
pre-push hook's G0 orchestrator-guard blocks any push not descended from publish.py).
The pipeline is migrated to the CPV canonical pipeline to clear the CPV advisory
**RC-PIPELINE-DRIFT-001** and satisfy 5 provenance MAJORs (done in commit f83f3b1,
shipped v0.1.6 = f6ebf48).

**Why:** a drifted pipeline is a CPV WARNING and the provenance gaps were MAJORs. The
canon bundles idempotent atomic push, SHA-pinned actions, per-job `timeout-minutes`,
env-sanitized `run:` blocks, actionlint + commitlint gates, a dedicated zizmor
workflow-security job, a macOS test matrix, and SLSA supply-chain controls.

**How to apply:**
- Publish with `uv run python scripts/publish.py --patch|--minor|--major` (no flag =
  auto-detect from conventional-commit types). Pipeline: bypass → clean-tree →
  ruff + mypy → pytest → CPV --strict → version-consistency → bump → README badge →
  git-cliff changelog → atomic push → GitHub release.
- CPV is PINNED at `@v2.153.4` at ALL callsites (publish.py gate + stage_validate +
  install_branch_rules; ci.yml Validate; release.yml). Why: the cold `uvx --from git+…`
  build is cached per tag, and a stricter FUTURE CPV release cannot red-light the gate
  with no plugin change. Bump this pin deliberately, in lockstep across all callsites,
  when adopting a newer CPV.
- `--gate` mode CANNOT be run standalone — its G0 guard only accepts the pre-push hook's
  process ancestry. To verify locally without the hook, run the stages directly:
  `uv run ruff check scripts/` · `uv run mypy scripts/ --ignore-missing-imports` ·
  `uv run pytest tests/ -q` ·
  `uvx --from git+<cpv-repo>@v2.153.4 --with pyyaml cpv-remote-validate plugin . --strict`.
- release.yml (tag push only) emits an SPDX **SBOM** (anchore/sbom-action), per-asset
  **SHA256SUMS**, and a build-provenance **attestation** (actions/attest-build-provenance;
  needs `id-token: write` + `attestations: write` on the job). Verify a downloaded asset
  with `gh attestation verify <asset> --repo <owner>/<repo>` (exit 0 = cryptographically
  verified against the repo's OIDC identity).
- `cpv.pipeline.intentional_divergence: [".mega-linter.yml"]` in plugin.json declares the
  one deliberately-customized canon file, so `cpv standardize --force-templates` will not
  clobber it. Preserve this array across canon re-syncs.
- The `cross-refs` workflow has a `paths:` filter (`agents|skills|commands/**/*.md` +
  `bin/amw-validate-cross-refs.sh` + its own yml). A version-bump-only or pipeline-only
  push does NOT trigger it — that is CORRECT (not a missing run); its last green stands.

See also: [[cpv-gate-blocked-by-hyperframes-submodule]] — the SECURITY / vendored-submodule
gate, a DIFFERENT axis from pipeline drift. Governed by [[architecture-hub]].

## Notes and lessons learned

[^1]: [ocd:2026-07-13 lmd:2026-07-13] The canon migration was authored by a background
  plugin-fixer agent that DIED on a session limit before committing. Its work was verified
  INDEPENDENTLY before commit (ruff + mypy scripts/ clean, pytest 238-pass/6-skip, CPV
  --strict @v2.153.4 = CRITICAL=0 MAJOR=0 MINOR=0 NIT=0) — NOT trusted from the agent's
  self-report. Lesson: when taking over a background agent's uncommitted work, re-run the
  objective gate yourself before committing; a dead agent's self-report is a claim, not
  evidence.
