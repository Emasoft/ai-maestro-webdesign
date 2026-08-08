---
name: baseline-ruleset-definition-unresolved
description: "should I add required_linear_history to baseline-history-protect / our branch ruleset looks drifted from the documented baseline / is restoring the ratified baseline safe here / why does the rule list not match the live repo"
ocd: 2026-08-08
lmd: 2026-08-08
metadata:
  node_type: memory
  type: project
  tier: component
---

# baseline-ruleset-definition-unresolved


^ATOM-DTYE-62MD [desc:"DO NOT add required_linear_history to match the documented baseline — the documented rule list has no provenance and adding it blocks merge commits", keywords: should_I_add_required_linear_history baseline-history-protect_looks_drifted restore_the_ratified_baseline_safely rule_list_does_not_match_the_live_repo manager-approval-defaults_section_F baseline-tag-protect_not_documented, type: project, ocd: 2026-08-08, lmd: 2026-08-08]

**HOLD — do not "restore" this. Verified on this repo 2026-08-08.**

`~/.claude/rules/manager-approval-defaults.md` §F documents
`baseline-history-protect` as `deletion` + `non_fast_forward` +
**`required_linear_history`**. This repo's live ruleset (id 18894431,
`enforcement: active`, `bypass_actors: []`) carries only:

```
baseline-history-protect -> deletion, non_fast_forward
baseline-pr-and-checks   -> deletion, non_fast_forward, pull_request, required_status_checks
baseline-tag-protect     -> deletion, update          <- live here, §F does not mention it at all
```

`required_linear_history` is on **no** ruleset on this repo. Every other §F
attribute (bypass_actors, enforcement, target) matches.

**The rule list has NO PROVENANCE.** §F cites `janitor#14` as the ratification.
That issue was read first-hand: **zero** occurrences of `required_linear_history`,
`non_fast_forward`, or `baseline-history-protect` anywhere in its body. The
prose asserts a definition the cited source does not contain.

**Why this is a trap rather than a to-do.** "Restore drifted branch rules back
to the ratified baseline" is an explicitly **Tier-0 EXEMPT** operation — no
approval required. So a future session comparing §F to reality sees drift,
correctly believes it needs no sign-off, and adds the rule in good faith.
`required_linear_history` **blocks merge commits**, on a repo that now takes
cross-plugin PRs. Good-faith, exempt, and damaging.

Fleet state is inconsistent in BOTH directions (three repos lack the rule; at
least one peer has since ADDED it to match the prose), so there is no
unambiguous "as-is" to restore to. Tracked upstream at `Emasoft/ai-maestro#140`.
Wait for the hub's answer; do not reconcile locally. [^1]

## Notes and lessons learned

[^1]: [id:ATOM-VELL-SSDT, status:valid, keywords:"the_rule_cites_a_ratification_issue is_the_cited_source_actually_the_source prose_asserts_a_definition exempt_operation_still_caused_damage follow_the_citation_before_restoring", ocd:2026-08-08, lmd:2026-08-08] DO NOT treat a documented baseline as the thing to restore toward just because the doc cites a ratification, BECAUSE §F cites `janitor#14` and that issue contains ZERO mentions of the rule list it is cited for — the citation exists, the provenance does not. DO open the cited source and confirm it says what cites it, ESPECIALLY when the resulting action is classified EXEMPT: exempt means no second pair of eyes, so a wrong premise there goes straight to production with nobody asked. An exempt operation is a reason for MORE verification, not less.
