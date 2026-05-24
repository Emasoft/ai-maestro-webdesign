# Technique catalog and Mode B gold-standard examples

Companion reference for [SKILL](../SKILL.md). The 12 JSON-render TECH files live alongside this one in `./references/`. The shared 95-pattern freeform catalog is at [ascii](../../amw-diagram-formats/references/ascii.md). When authoring, pick **at least 10 distinct TECH-IDs per variant** so each diagram demonstrates deliberate construction rather than a single-source port.

## Representative TECH-IDs from rebuilt demo variants

These are working combinations the plugin's reference demos use — copy the shape, then swap in your own labels.

- **Baseline dashboard** — TECH-02 (3-line buttons), TECH-03 (multi-line titled cards), TECH-23 (pipe-column table), TECH-38 (`[!]` markers), TECH-90 (band rules with T-junctions).
- **Advanced dashboard** — TECH-22 (timeline axis), TECH-46 (axis labels), TECH-82 (editorial brand), TECH-84 (hero narrative).
- **Experimental dashboard** — TECH-11 (UPPERCASE section labels), TECH-83 (three-column editorial), TECH-84 (LEAD story), TECH-85 (in-cell metric arithmetic).

The full description of each TECH-NN code is in the shared 95-pattern catalog at [ascii](../../amw-diagram-formats/references/ascii.md).

## Mode B gold-standard inspiration

For non-trivial Mode B wireframes (multi-stage flows, fan-out/fan-in, rich multi-line boxes), copy one of three canonical examples and edit labels + topology to match the brief. Frame-width and vertical-alignment invariants are already validator-correct in the source, so the validator passes on first try for minor label swaps — most iteration cost is on structural changes, not cosmetic ones.

| File | Shape | Use as template for |
|---|---|---|
| [`../../amw-box-diagram/examples/incident-response.txt`](../../amw-box-diagram/examples/incident-response.txt) | 5-stage flow (ALERT / TRIAGE / MITIGATE-INVESTIGATE-COMMUNICATE / VERIFY / POST-MORTEM); each box 5-7 body lines; mid-flow 3-way fan-out then fan-in | "Complex process" Mode-B diagrams (runbooks, incident playbooks) |
| [`../../amw-box-diagram/examples/ci-cd-pipeline.txt`](../../amw-box-diagram/examples/ci-cd-pipeline.txt) | 3-stage pipeline; fan-out to 3 parallel tests; fan-in to Release; 2-way fan-out to Staging + Production | "Branching deploy" diagrams (CI/CD, build pipelines) |
| [`../../amw-box-diagram/examples/microservices.txt`](../../amw-box-diagram/examples/microservices.txt) | Browser/Mobile → LB → API Gateway → 3 services (Auth/User/Order) → data stores (Redis/Postgres/MongoDB) + Queue → Worker → S3 | "System architecture" diagrams (service maps, dependency graphs) |

## Cross-references

- [SKILL](../SKILL.md) — the parent skill (Mode A / Mode B authoring).
- [SKILL](../../amw-ascii-validator/SKILL.md) — validator tool-chain.
- [SKILL](../../amw-box-diagram/SKILL.md) — origin of the three gold-standard examples.
- [ascii](../../amw-diagram-formats/references/ascii.md) — shared 95-pattern freeform catalog and per-source breakdown.
