# amw-text-visual-workflows — Diagram archetype examples

Three workflow archetypes — flowchart (branching logic), linear timeline with calendar markers, swimlane (parallel tracks). Pick one per artifact — do not merge them.

## 1. Flowchart — branching logic

Use when the workflow has decisions with yes/no or multi-way branches.

Glyphs:

- Start / End: `(start)` `(end)`
- Process step: `[ action ]`
- Decision: `{ condition? }`
- Sync arrow: `-->`
- Emphasized arrow: `==>`
- Async / eventual arrow: `~~>`

```
(start)
  |
  v
[ Open PR ]
  |
  v
{ Checks pass? }
  |       |
  yes     no
  |       |
  v       v
[ Review] [ Fix + push ]
  |           |
  |           '--> back to checks
  v
[ Merge ]
  |
  v
(end)
```

## 2. Timeline — linear sequence with calendar markers

Use when time ordering and calendar position are the point (launch schedules, onboarding weeks, migration phases).

```
Day 0     Day 3     Day 7     Day 14
|---------|---------|---------|
Plan      Build     QA        Launch
@alice    @bob      @cara     @dana
```

The vertical bars `|` mark the anchor dates; horizontal dashes `-` fill the gap proportional to the interval, not to character count. Annotate each anchor with owner / phase label underneath.

## 3. Swimlane timeline — parallel tracks

Use when multiple roles / teams are working in parallel and you want to show who owns what over time.

```
          Day 0     Day 3     Day 7     Day 14
Dev       |==build==|==test==|
QA                  |==plan==|==run====|
Launch                                 |==go=|
```

Each row is one lane; `==` fills the active window for that lane on that date range.
