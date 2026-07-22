# ROADMAP — eval-anything

Honest coverage: the scaffold generated the spine below; these were **declared in the
spec but NOT auto-generated** (no fake passes — each is a real next turn):

- [x] Replace scaffold seed content in `data/` with the first real increment
      (2026-07-22: 253 web-verified entries across 6 datasets, `make check` green,
      ledgered in News).

## Next turn

- [ ] **Publish** — create `github.com/wjlgatech/eval-anything` and push (human-gated
      outward action; CI + weekly sync workflows are already in `.github/workflows/`).
- [ ] **Super-tool depth** — grow `skills/eval-anything/SKILL.md` beyond the scaffold
      contract: "pick me a benchmark" routing over `data/registry.yml`, an eval-design
      checklist wired to the loop's judge/gate stages (maker≠checker, bias checks,
      error bars).
- [ ] **Leaderboard watch** — consider tracking non-GitHub surfaces the registry can't
      sync (Arena, SEAL, Epoch Benchmarking Hub, HLE leaderboard) via a `watch.yml` +
      freshness probe, honest-null on scrape failure.
- [ ] **Split criterion review** — revisit the guardrails/security in-repo decision if
      that fold's entry count rivals the measurement content (currently 47 vs ~206).

## Standing

- Weekly `make sync` (human-gated PR) keeps the 54-repo registry honest.
- Every score cited from here must name benchmark VERSION + contamination status
  (non-negotiable #3).
