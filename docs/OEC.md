# OEC — Observe → Evaluate → Control: the deep dive

The distilled canon lives in `data/oec.yml` (rendered into the README). This doc holds
the narrative that doesn't fit a table row. Researched and web-verified 2026-07-22 via
three survival-test sweeps (300y / 30y / now horizons).

## The frame (Paul Wu, 2026-07-22)

1. **Observability precedes eval** — you cannot evaluate what you cannot observe.
2. **Eval targets the objective, not just the engineering** — "is the code sound?" AND
   "is the business objective on track?", across design → planning → execution →
   maintenance → upgrade.
3. **Eval without control is a scoreboard** — after eval come decisions and change.

Kalman (1960) proved observability and controllability are mathematical **duals** — a
system is observable iff its transpose is controllable. The O and the C were born twins;
OEC is a theorem, not a metaphor.

**The OEC name collision that is actually a complement:** Ron Kohavi's **OEC — Overall
Evaluation Criterion** — is the single composite metric an online experiment optimizes,
"measurable in the short term yet believed to causally drive long-term strategic
objectives." Kohavi's OEC is the formalized **E** inside the larger O→E→C cycle: the
experiment platform observes, the OEC evaluates, the ship/no-ship decision is the control.

## The cross-century quote pair that frames the whole domain

> "When you can measure what you are speaking about, and express it in numbers, you know
> something about it; but when you cannot measure it… your knowledge is of a meagre and
> unsatisfactory kind." — **Lord Kelvin, 1883**

> "It is wrong to suppose that if you can't measure it, you can't manage it — a costly
> myth." — **W. Edwards Deming, 1993**

Both poles survived. The tension between them **is** the discipline.
(Related folklore, verified: "what gets measured gets managed" was **never said by
Drucker**; its likely written origin is Ridgway 1956 — *a paper warning against it*.)

## Verified corrections (citation-rigor findings from the sweeps)

- DuPont ROI formula: **1912–14**, not the commonly-cited 1919 (Hagley Library).
- McNamara fallacy: coined by **Yankelovich, Oct 1971**, not 1972.
- Campbell's law: Dec **1976** occasional paper; journal-published 1979.
- Maxwell's "On Governors" (1868) was **ignored for ~80 years** until Wiener revived it —
  its canonization was retroactive, not inevitable.
- A claimed 2026 "OpenAI acquires promptfoo" circulated in secondary sources but could
  **not be verified** against a primary source this run — excluded from the registry
  (unverifiable caps at WEAK).

## The anti-portfolio — era-matched corpses

Frameworks that were louder at birth than most survivors, and are dead or niche today.
Every corpse is a lesson in what kills an OEC loop.

**300y window:**
- **PPBS** (McNamara's DoD, 1961; government-wide 1965) — abandoned 1971. Died of the
  fallacy named after its patron, while its contemporaries PERT and CBA survived.
- **Taylorist stopwatch piece-rates** (1911) — Congress banned stopwatch studies in
  arsenals; the ideology died, only the measurement residue survived.
- **Project Cybersyn** (Beer, Chile 1971-73) — the most ambitious real-time economic
  control room ever built; died with the 1973 coup.
- **US quality-circle fad** (1979-85) — copied the TPS ritual without transferring
  control to the observer; the andon cord survived, its imitation died.
- **Forced ranking / vitality curve** (GE 1980s) — dropped by Microsoft 2013 and GE
  itself 2015; Goodhart/Campbell applied to humans.

**30y window:**
- **Microsoft Viva Goals / Ally.io** — bought at the OKR-hype peak 2021, retired 2025-12
  with no replacement. The OKR practice survived; the hyped tooling did not.
- **Holacracy** — Medium abandoned it 2016; Zappos quietly backed away.
- **Stack ranking** — the same corpse in a newer suit.
- **Rules-based multi-touch attribution** — deprecated by Google in GA4 (2023);
  the promise of user-level truth collapsed under privacy.
- **Klout Score** — shut down 2018; the cautionary tale for single-number metrics with
  no causal link to value.

## The Lindy readings (one per horizon)

- **300y:** the deepest survivors fused O, E, and C **into a single artifact a worker
  could use** — ledger, control chart, PID loop, checklist, andon cord. Every corpse in
  the anti-portfolio is a framework a consultant could sell; every 🏛 survivor is an
  artifact. And the warnings cohort (Goodhart/Campbell/McNamara, all born 1971-76) is the
  youngest cluster yet the fastest-rising: the *limits* of measurement are becoming as
  load-bearing as measurement itself.
- **30y:** the survivors are **closed loops with a control action attached**, not
  scoreboards. Error budgets gate releases; experiments gate ships; WBR metrics have
  owners and get retired; OKRs force a quarterly re-decision. The faded items were either
  structures without evaluation or scores without actuators. In one line: *observation is
  cheap, evaluation is hard, and the scarcest asset is a trustworthy mechanism that turns
  evaluation into action.*
- **now:** **O is standardizing** (OTel GenAI semconv, MCP trace context), **C is
  consolidating** (Statsig→OpenAI, Eppo→Datadog — experimentation platforms became the AI
  control plane), **E-of-business is professionalizing** (error-analysis-first doctrine +
  economic evals). The load-bearing joint: online judge scores can only *gate* rollouts
  if the judges were first validated against humans. The biggest gaps: no native drift
  detection with auto-baselining in OSS trace platforms; "AI SLOs" have no canonical
  owner; only ~21% of enterprises have mature agent governance — **C is the least-built
  pillar despite the most vendor activity.**

## How this repo's loop maps onto OEC

| Repo stage | OEC pillar |
|---|---|
| scope | E — the objective made a measurable claim (double-loop learning questions it) |
| collect, run | O — provenance, versions, reproducible observation |
| judge | E — maker≠checker, bias-mitigated, uncertainty reported |
| gate | C — pass/fail with consequences |
| compound | C — what moved feeds the next cycle (kaizen) |
