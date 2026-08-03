# ROADMAP — eval-anything

Honest coverage: the scaffold generated the spine below; these were **declared in the
spec but NOT auto-generated** (no fake passes — each is a real next turn):

- [x] Replace scaffold seed content in `data/` with the first real increment
      (2026-07-22: 253 web-verified entries across 6 datasets, `make check` green,
      ledgered in News).

## Next turn

- [x] **Publish** — `github.com/wjlgatech/eval-anything` live (private, matching the
      family), CI green on `main` (2026-07-22); weekly sync workflow armed.
- [x] **The agentic-tooling eval map** — `data/tooling.yml` (2026-08-03): 12 tooling
      primitives (skill · tool · mcp-server · harness · subagent · workflow ·
      context-compiler · memory · hook · permission-model · plugin · judge), each with
      its URL-verified benchmarks, a coverage grade, an evidence tier, and a
      `cost_metric` column. Answers "should we adopt the community's 1M skills?" by
      showing it is a question about ONE of twelve primitives. Gated: `coverage: none`
      ⟺ zero benchmarks, enforced both directions, with 5 tests that prove the gate
      can fail (it caught a real honesty gap in `mcp-server` on first run).
- [ ] **Cost-per-kilotoken (the metric the field is missing)** — `data/tooling.yml`
      records that only 1 of 12 primitives has its context cost measured anywhere.
      Build `Δ pass-rate / Δ context tokens` as a scored gate: a primitive adding
      +2pp for 8k tokens must fail. This is where the repo CONTRIBUTES rather than
      tracks. Blocked on nothing — needs a paired-eval runner (SkillsBench's matched
      with/without design is the template).
- [ ] **Trust ≠ relevance (cross-repo P0, filed 2026-08-03)** — `anyagent skills find`
      grades trust (license + code-shipping) but not relevance, and **passes a gate on
      a safe-but-irrelevant hit**: querying "write a react component with tests"
      returned `52-newsletter-ideas` at 87/100 ✅ trusted and PASSED `--gate 1`. The two
      axes are orthogonal and must BOTH clear a bar. Fix lives in the `anyagent` repo;
      the failure mode is what `SkillResolve-Bench` measures (see `data/tooling.yml`).
- [x] **OPEN SOURCE** (2026-08-03) — repo is PUBLIC at github.com/wjlgatech/eval-anything,
      Apache-2.0 (`scripts/`) + CC BY 4.0 (`data/`), with `CONTRIBUTING.md` making the
      add-one-row model executable. The recorded reason for privacy ("matching the family")
      was measured false: the declared family was 5 PUBLIC / 4 private. Pre-flip audit found
      zero secrets across all commits; an unreleased sibling product's walkthrough was purged
      from history with `git filter-repo`
      (verified by exhaustive fresh-clone object scan, not local refs — a local-only check
      reported clean while a stale `sync/weekly` branch still carried it).
- [ ] **Contamination status is not yet a field** — non-negotiable #3 says every score names
      its benchmark VERSION and contamination status, and CONTRIBUTING now demands it of
      contributors, but no `data/` schema actually holds it. Right now the discipline lives in
      prose, which means it is unenforced. Add `version` + `contamination` to the benchmark
      shape in `data/tooling.yml` and gate it in `validate.py` — otherwise rule 3 is exactly
      the kind of claim-without-evidence this repo exists to catch.
- [ ] **Super-tool depth** — grow `skills/eval-anything/SKILL.md` beyond the scaffold
      contract: "pick me a benchmark" routing over `data/registry.yml`, an eval-design
      checklist wired to the loop's judge/gate stages (maker≠checker, bias checks,
      error bars).
- [ ] **Leaderboard watch** — consider tracking non-GitHub surfaces the registry can't
      sync (Arena, SEAL, Epoch Benchmarking Hub, HLE leaderboard) via a `watch.yml` +
      freshness probe, honest-null on scrape failure.
- [ ] **Split criterion review** — revisit the guardrails/security in-repo decision if
      that fold's entry count rivals the measurement content (currently 47 vs ~206).
- [ ] **Deploy the brief webapp** — Vercel project `eval-anything-demo` (root `brief/`),
      then add ANTHROPIC_API_KEY so the copilot answers via Claude (human-gated:
      identity + spend); set `demo_url` in data/meta.yml so the README callout renders.
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
