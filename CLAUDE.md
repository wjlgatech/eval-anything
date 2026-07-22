# CLAUDE.md — eval-anything

Part of the `-anything`/`-os` family (`anyagent`, `FM-os`, `rsi-os`, `longevity-loop`, `animate-anything`, `master-anything`, `marketing-anything`, `graph-engineering-anything`, `loop-engineering-anything`).
Method lineage: `anyagent` — never self-certify; the check is the only truth.

## What this repo is

One reliable place for evaluation of foundation models (LLM, VLM, VLA) and agentic systems — and the guardrails/security that adversarially test them. Tracks the field's load-bearing harnesses, benchmarks, papers, labs, and people (lm-evaluation-harness, HELM, Inspect, SWE-bench, LLM-as-judge and its biases, red-teaming), tiers every claim by evidence, and ships tooling to design and run evals with Claude.


Profile: **data-compiled**. Loop: `scope → collect → run → judge → gate → compound`.

Three folds, one closed loop (the baseline contract):
- 📚 **Knowledge** — an evidence-tiered map of the eval field — harnesses, benchmarks, seminal papers, canonical blogposts, labs, and people across LLM/VLM/VLA/agentic eval AND guardrails/security — synced weekly so this is the one place to track what matters
- 🛠️ **Tooling** — the /eval-anything super-tool — design an eval, pick the right benchmark/harness, run LLM-as-judge with bias checks, red-team an agent — no eval expertise required
- 🤝 **Community** — add-one-row registry PRs, weekly human-gated sync with "what moved", saturated/contaminated benchmarks flagged for review — never silently kept as evidence

This is a **meta-repo**: it tracks top-rated upstream repos (data/registry.yml),
synced weekly so people rely on it as the one place for what matters in this domain.

## The one rule that matters

NEVER hand-edit README.md or any generated artifact — the source of truth is `data/*.yml`; edit it and run `make build`. CI drift-gates this.

## Build & check

```bash
make check   # THE finish line — CI runs exactly this on every push/PR
make help    # every target, self-documented
```

## The non-negotiables

- No evidence ⇒ no claim. Unmeasured is 'not measured' (excluded), never a fake pass. Record the null ('none found') rather than fabricate.
- Maker ≠ checker. Nothing grades its own homework — an independent rubric/script/CI verifies the work.
- An honest ❌ beats a fake ✅. `make check` is the only truth; never hand-report green.
- Never hand-edit generated files. Edit the source of truth and regenerate; CI drift-gates it.
- Human-gated irreversibles. Publish/post/pay/delete actions are drafted by the agent, shipped by the human — permanently.
- Compose, never absorb. Call third-party engines and cite provenance (pin commits/URLs); never fork-and-copy content.
- Citation rigor (Nature/NeurIPS standard): cite the primary source (paper/DOI/repo), never the trade article that covered it; secondary-only evidence is marked 'as cited in' and caps at WEAK until the primary is read.
- Maker≠checker is doubly binding here: LLM-as-judge carries documented position, verbosity, and self-preference biases — no judge score counts as evidence without a stated bias-mitigation (randomized order, reference-guided, or human-calibrated sample).
- Every reported score names the benchmark VERSION and contamination status; saturated or contaminated benchmarks are flagged and never cited as headline evidence.
- Guardrails/security is a first-class fold of evaluation (red-teaming IS adversarial eval); it splits into a sibling repo only when that fold demonstrably outgrows this one.

## Gotchas

- YAML boolean/null trap: quote enum-ish values ('on', 'off', 'yes', 'null') in data files — PyYAML coerces them (bit longevity-loop twice).
- Tests must not mutate tracked files; exercise WRITE paths in a tempdir (write-path bugs hide behind read-only --check).
- Link checks: accept bot-unfriendly codes [200,202,206,403,405,406,415,429] in lychee.toml — don't let false negatives block CI.
- LLM-as-judge is NOT a free lunch — position bias, verbosity bias, and self-preference are measured effects (Zheng et al. 2023, arXiv:2306.05685); calibrate against human labels before trusting.
- Leaderboard deltas within a few points are often noise — report confidence intervals, not single numbers (Anthropic's 'statistical approach to model evals', 2024).
- A benchmark's public test set is in every frontier model's pretraining shadow — treat unversioned scores on pre-2024 benchmarks as contaminated until shown otherwise.

## Identity

Personal identity ONLY: author/push as `wjlgatech` (wjlgatech@gmail.com). Never the
Accenture identity; never push to an Accenture host.
