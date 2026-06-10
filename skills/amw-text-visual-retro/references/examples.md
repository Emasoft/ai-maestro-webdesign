# amw-text-visual-retro — Template archetype examples

## Table of Contents

- [1. Grid (categories side-by-side)](#1-grid-categories-side-by-side)
- [2. Milestone timeline](#2-milestone-timeline)
- [3. Heatmap](#3-heatmap)

Three retro template archetypes — grid (categories side-by-side), milestone timeline (temporal story), heatmap (density readout). Pick one per artifact — do not merge them.

## 1. Grid (categories side-by-side)

Use for `start/stop/continue`, `went well / needs attention`, `4Ls` (liked / learned / lacked / longed-for), or any two-to-four-category split.

```
+----------------------------+-----------------------------+
| Went Well                  | Needs Attention             |
+----------------------------+-----------------------------+
| Deploy automation shipped  | Flaky tests blocked 3 PRs   |
| @alice, done               | @bob owns fix (due 04-28)   |
|                            |                             |
| +12% DAU post-launch       | Support ticket backlog +40% |
| metric: dau_daily          | @triage-team to prioritize  |
+----------------------------+-----------------------------+
```

## 2. Milestone timeline

Use for launch post-mortems or experiment readouts where the story is temporal.

```
Week 1      Week 2      Week 3      Week 4
|-----------|-----------|-----------|-----------|
Plan        Build       QA          Launch      Post
@alice      @dev-team   @qa-team    @launch     @all

Highlights:
  Week 2 -- migration framework shipped (PR #123)
  Week 3 -- 2 p0 bugs caught (one leaked to prod, see incident #42)
  Week 4 -- soft launch succeeded, +12% DAU

Actions:
  [ ] Fix incident #42 runbook (@oncall, due 04-28)
  [ ] Remove dead migration code (@db-team, due 05-05)
```

## 3. Heatmap

Use for density / frequency readouts — incident count per day, experiment exposure per segment, error rate per endpoint.

Legend for intensity markers (from low to high): `[ ]`  `[~]`  `[+]`  `[++]`  `[!]`. Use exactly this set — anything else breaks the column alignment.

```
              Mon   Tue   Wed   Thu   Fri   Sat   Sun
incidents    [ ]   [~]   [+]   [!]   [++]  [ ]   [ ]
deploys      [+]   [+]   [+]   [+]   [+]   [ ]   [ ]
on-call      [ ]   [ ]   [ ]   [!]   [!]   [ ]   [ ]

Legend: [ ] 0,  [~] 1,  [+] 2-3,  [++] 4-6,  [!] 7+
```
