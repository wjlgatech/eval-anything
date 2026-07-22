# ROADMAP — eval-anything

Honest coverage: the scaffold generated the spine below; these were **declared in the
spec but NOT auto-generated** (no fake passes — each is a real next turn):

- [x] Replace scaffold seed content in `data/` with the first real increment
      (2026-07-22: 253 web-verified entries across 6 datasets, `make check` green,
      ledgered in News).

## Next turn

- [x] **Publish** — `github.com/wjlgatech/eval-anything` live (private, matching the
      family), CI green on `main` (2026-07-22); weekly sync workflow armed.
- [ ] **Super-tool depth** — grow `skills/eval-anything/SKILL.md` beyond the scaffold
      contract: "pick me a benchmark" routing over `data/registry.yml`, an eval-design
      checklist wired to the loop's judge/gate stages (maker≠checker, bias checks,
      error bars).
- [ ] **Leaderboard watch** — consider tracking non-GitHub surfaces the registry can't
      sync (Arena, SEAL, Epoch Benchmarking Hub, HLE leaderboard) via a `watch.yml` +
      freshness probe, honest-null on scrape failure.
- [ ] **Split criterion review** — revisit the guardrails/security in-repo decision if
      that fold's entry count rivals the measurement content (currently 47 vs ~206).
- [ ] **OEC gap watch** — the now-horizon research surfaced three unowned gaps worth
      tracking (and possibly building toward): (1) no OSS trace platform ships native
      drift-detection with auto-baselining; (2) "AI SLOs" have no canonical owner;
      (3) only ~21% of enterprises have mature agent governance — C is the least-built
      pillar. Each is a candidate for a future tooling increment.
- [ ] **Verify the promptfoo-acquisition rumor** when a primary source appears — the
      claim was removed from the registry under citation rigor (docs/OEC.md).

## Standing

- Weekly `make sync` (human-gated PR) keeps the 54-repo registry honest.
- Every score cited from here must name benchmark VERSION + contamination status
  (non-negotiable #3).
