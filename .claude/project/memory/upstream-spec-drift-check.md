---
name: upstream-spec-drift-check
description: "has the ai-maestro role-plugins spec changed since we conformed / how do I check for upstream spec drift / which spec governs webdesign / why does querying main give a stale or 404 answer / what blob sha are we conformant against"
ocd: 2026-08-08
lmd: 2026-08-08
metadata:
  node_type: memory
  type: project
  tier: component
---

# upstream-spec-drift-check


^ATOM-DBP3-WQY8 [desc:"webdesign is governed by role-plugins-spec.md on the governance-rules branch; poll its per-FILE blob sha, never the branch sha", keywords: which_spec_governs_webdesign how_do_I_check_for_upstream_spec_drift has_the_role-plugins_spec_changed why_does_main_return_stale_or_404 governance-rules_branch_not_main blob_sha_change_signal 3P-VER-05 what_version_are_we_conformant_against, type: project, ocd: 2026-08-08, lmd: 2026-08-08]

**The governing document is `design/specs/role-plugins-spec.md` in
`Emasoft/ai-maestro`, on the UNMERGED `governance-rules` branch — not `main`.**
Querying `main` does not error usefully: it serves an older `GOVERNANCE-RULES.md`
and 404s the spec paths, so a consumer doing the obvious thing gets a coherent,
confident, WRONG answer with nothing in the response saying so.

```bash
gh api "repos/Emasoft/ai-maestro/contents/design/specs/role-plugins-spec.md?ref=governance-rules" --jq .sha
```
 [^1]


^ATOM-6F34-XFQN [desc:"poll the per-FILE blob sha as the change signal; the branch commit sha is FORBIDDEN because it manufactures false confidence", keywords: how_do_I_poll_for_spec_changes branch_sha_vs_blob_sha 3P-VER-05_change_signal why_is_the_branch_commit_sha_forbidden polling_says_current_but_the_doc_is_stale, type: project, ocd: 2026-08-08, lmd: 2026-08-08]

**Poll the per-FILE blob sha; the branch commit sha is FORBIDDEN as a change
signal** — `3P-VER-05` (`3-pillars-spec.md`, spec-version 1.7.0). It fails in the
dangerous direction: the branch sha moves on every unrelated commit, so a
consumer polls, sees movement, refetches, gets byte-identical bytes, and records
"checked, current" — manufacturing confidence instead of supplying information.
Silence would be safer. Measured upstream: the branch sha moved across four
unrelated commits while the spec blob sat unchanged for 13 days, serving 1.1.1
against a working copy at 1.5.0.


^ATOM-NETA-ZTMZ [desc:"conformance point of record: role-plugins-spec blob 7757c76f75fc at spec-version 1.0.1, as of webdesign v0.1.9", keywords: what_blob_sha_are_we_conformant_against which_spec-version_did_we_conform_to conformance_point_of_record has_the_spec_moved_since_we_last_checked, type: project, ocd: 2026-08-08, lmd: 2026-08-08]

**Conformance point of record — 2026-08-08, webdesign v0.1.9.**
`design/specs/role-plugins-spec.md` @ `governance-rules`, blob
`7757c76f75fc249e3b2ac9df72b37bc4833d9dad`, `spec-version: 1.0.1`.
A different blob sha means the spec moved: re-read it before citing any clause. [^2]


^ATOM-BE2Y-JJYJ [desc:"the canonical six-sha fingerprint does NOT cover role-plugins-spec.md — watching it would leave webdesign's governing doc unwatched", keywords: does_the_six_sha_fingerprint_cover_us which_files_are_in_the_canonical_fingerprint is_role-plugins-spec_in_the_fingerprint what_should_webdesign_actually_watch, type: project, ocd: 2026-08-08, lmd: 2026-08-08]

**The canonical fingerprint does NOT cover the file that governs us.**
`3P-VER-05` defines a "six shas" fingerprint — read it closely: those six are
`3-pillars-spec.md` **plus its five `rules/aimaestro/` overlays**. They do NOT
include `role-plugins-spec.md`, and do NOT include `GOVERNANCE-RULES.md`.
So watching the sanctioned six leaves webdesign's ONE governing document
unwatched. **Watch our own file**; treat the six as a different pillar's
fingerprint. (A peer relayed the six as the complete fingerprint while also
listing `GOVERNANCE-RULES.md` inside it — seven items called six — and omitted
`role-plugins-spec.md` entirely. Verified against the clause text directly.)

## Notes and lessons learned

[^1]: [id:ATOM-LVBG-L3ED, status:valid, keywords:"a_spec_clause_I_cited_was_reversed why_did_we_ship_a_wrong_citation is_the_served_spec_the_current_spec an_amendment_not_served_is_not_published pin_the_spec-version_in_every_citation", ocd:2026-08-08, lmd:2026-08-08] DO NOT cite a clause from this spec without also reading its `spec-version:` line and pinning that version in the citation, BECAUSE an amendment the authority does not SERVE is not published however correct its text — webdesign shipped v0.1.8 citing RP-MODEL-01 from spec-version 1.0.0 hours before learning 1.0.1 had REVERSED that exact clause, and nothing in the 1.0.0 fetch hinted a newer text existed. DO record the blob sha + spec-version you conformed against (this page's atom), and re-check the blob before re-citing.
[^2]: [id:ATOM-4Z10-7ZEM, status:valid, keywords:"the_blob_sha_moved_what_changed is_a_changed_sha_enough_to_act_on do_I_need_to_re-read_after_a_sha_change stamp_is_a_prompt_not_a_substitute", ocd:2026-08-08, lmd:2026-08-08] DO NOT treat a changed blob sha as telling you WHAT changed, BECAUSE a sha is a one-bit signal — it says these bytes differ, never which clause moved or whether the change even touches you. The stamp is a prompt to RE-READ, not a substitute for reading. DO re-fetch the document and re-check the specific clauses you cite whenever the sha differs from the recorded one; and keep the read-DATE beside the sha, because an undated pin cannot go stale, it can only be silently wrong.
