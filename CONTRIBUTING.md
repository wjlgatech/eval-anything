# Contributing

The whole contribution model is **add one row**. You don't need to understand the build,
the loop, or the OEC frame to make this repo better — you need one entry backed by one
primary source.

## The 60-second version

```bash
git clone https://github.com/wjlgatech/eval-anything.git && cd eval-anything
$EDITOR data/registry.yml     # or papers.yml, tooling.yml, security.yml, people.yml, …
make check                    # THE finish line — CI runs exactly this
```

**Never edit `README.md`.** It is generated from `data/*.yml`. Edit the data, run
`make build`, commit both. A drift gate fails the PR if the committed README doesn't match
what the data generates — that gate exists so the docs cannot lie about the data.

## The five rules that actually get a PR merged

These are the repo's non-negotiables. They are also the only things a reviewer will push
back on, so knowing them up front saves a round trip.

1. **No evidence ⇒ no claim.** Every row links its **primary** source — the paper, the DOI,
   the repo — never the article that covered it. Secondary-only evidence is marked as such
   and caps at WEAK until someone reads the primary.
2. **Record the null.** If you looked and found nothing, say so. `coverage: none` with an
   empty `benchmarks: []` is a *contribution*, not a gap. In `data/tooling.yml` the schema
   gate enforces this **both directions**: you cannot claim coverage without citing a
   benchmark, and you cannot mark something uncovered while listing one.
3. **Name the version and the contamination status.** A benchmark score without a version is
   unfalsifiable. Scores move between versions — SkillsBench's own numbers changed between
   its February and June revisions. If a benchmark's test set predates 2024, treat it as
   contaminated until shown otherwise and say so in the row.
4. **An honest ❌ beats a fake ✅.** If `make check` is red, send it red with a note, or fix
   it. Never hand-report green.
5. **A judge score is not evidence without a stated bias mitigation.** LLM-as-judge carries
   documented position, verbosity and self-preference biases. Cite randomized order,
   reference-guided grading, or a human-calibrated sample — or don't cite the score.

## Things that will get a PR declined

- Editing a generated file (`README.md`, `brief/data.js`) instead of its source.
- A benchmark row whose URL you did not open.
- A quotation that is actually a *summary* of the source. If a source is paywalled, you may
  **describe** its argument and cite it — you may not put it in quotation marks.
- Adding a promotional link for your own tool without an evidence tier and a "why tracked"
  that says what it's **bad** at too.
- Fabricating a plausible URL for a well-known benchmark. If you haven't read the primary,
  say so in the row's `gap` field and leave the URL out — that is what we do for BFCL,
  tau-bench and Terminal-Bench today.

## Disputes are welcome, explicitly

Coverage grades, evidence tiers and `cost_metric` values are **our editorial judgement**.
If you think a row is wrong, open an issue titled `dispute: <row>` and say what you read.
A corrected row is worth more than a new one. See `LICENSE-DATA` for the no-warranty terms
this operates under.

## Licensing your contribution

By opening a PR you agree your contribution is licensed the same way as the file you
touched: **Apache-2.0** for `scripts/`/`tests/`, **CC BY 4.0** for `data/`/`specs/`.

## Where things live

| Path | What |
|------|------|
| `data/*.yml` | the source of truth — everything published is generated from here |
| `data/tooling.yml` | the 12-primitive agentic-tooling eval map (coverage · evidence · cost) |
| `scripts/validate.py` | the schema gate — read it to learn what a valid row looks like |
| `scripts/build.py` | README generator; `make drift` proves the committed README matches |
| `tests/` | seam tests, including ones that assert the gates **fail** on a violation |
| `docs/ROADMAP.md` | open work, including what is honestly unbuilt |

Run `make help` for every target.
