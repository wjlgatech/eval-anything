#!/usr/bin/env python3
"""build.py — GENERATE README.md from data/*.yml (single source of truth).

`--check` = drift gate: fails when the committed README differs from the
regenerated one. Never hand-edit README.md.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REG_CATS = [
    ("harness", "🧰 LLM eval harnesses & platforms"),
    ("agent", "🤖 Agentic benchmarks & infrastructure"),
    ("vlm", "🖼️ VLM eval"),
    ("vla", "🦾 VLA / embodied eval"),
    ("judge", "⚖️ LLM-as-judge & arenas"),
    ("live", "📆 Live / contamination-resistant"),
    ("security", "🛡️ Guardrails & security"),
]
PAPER_CATS = [
    ("benchmarks", "Foundational capability benchmarks"),
    ("judge", "LLM-as-judge & eval methodology"),
    ("agentic", "Agentic & coding-agent evaluation"),
    ("vlm", "VLM evaluation"),
    ("vla", "VLA / embodied evaluation"),
    ("meta", "Meta-science of evaluation"),
]
LAB_CATS = [
    ("independent", "Independent eval orgs"),
    ("government", "Government & institutes"),
    ("academic", "Academic"),
    ("industry", "Industry eval teams"),
]
BLOG_CATS = [
    ("practitioner", "Practitioner blogs & seminal posts"),
    ("org", "Canonical org blogposts"),
]
PEOPLE_CATS = [
    ("architects", "Benchmark architects"),
    ("arena", "Arena & preference-based evaluation"),
    ("builders", "Frontier-lab & rising benchmark builders"),
    ("science", "Eval science, critique & rigor"),
    ("safety", "Agent, safety & dangerous-capability evaluation"),
    ("vla", "VLA / robotics / physical-AI evaluation"),
]
SEC_CATS = [
    ("standards", "Standards & governance frameworks"),
    ("papers", "Seminal papers"),
    ("tools", "Notable tools & concepts (beyond the tracked registry)"),
    ("agentsec", "Agent-specific security"),
    ("labs", "Labs & companies"),
    ("people", "Key people"),
]
OEC_PILLARS = [
    ("observe", "👁️ Observe — you can't evaluate what you can't observe"),
    ("evaluate", "⚖️ Evaluate — is the objective on track? (engineering AND business)"),
    ("control", "🎛️ Control — decisions and change close the loop"),
]
HORIZONS = {"300y": "🏛️ 300y", "30y": "🧭 30y", "now": "⚡ now"}


def load(name):
    f = ROOT / "data" / name
    return (yaml.safe_load(f.read_text()) or []) if f.exists() else []


def grouped(entries, cats, row_fn, header, level="###"):
    """Render one table per category, in declared order."""
    out = []
    for key, title in cats:
        rows = [row_fn(e) for e in entries if e.get("category") == key]
        if rows:
            out.append(f"{level} {title}\n\n{header}\n" + "\n".join(rows))
    return "\n\n".join(out)


def render() -> str:
    m = yaml.safe_load((ROOT / "data" / "meta.yml").read_text())
    stages = m["loop"]["stages"]
    loop_rows = "\n".join(
        f"| {i+1} | **{st['name']}** | {st['promise']} |" for i, st in enumerate(stages))
    fam_rows = "\n".join(
        f"| [`{f}`](https://github.com/{f}) | sibling — shared method lineage |"
        for f in m["family"])
    arrow = " → ".join(st["name"] for st in stages)
    gh = m["github"]
    badges = (
        f"[![CI](https://img.shields.io/github/actions/workflow/status/{gh}/ci.yml"
        f"?style=flat-square&label=check)](https://github.com/{gh}/actions)\n"
        f"[![Last Updated](https://img.shields.io/github/last-commit/{gh}"
        f"?style=flat-square&label=last%20turn)](https://github.com/{gh}/commits)\n"
        f"![License](https://img.shields.io/badge/license-{m['license'].replace('-', '--')}-lightgrey?style=flat-square)")
    news = ""
    items = load("news.yml")
    if items:
        rows = "\n".join(f"- **{n['date']}** — {n['entry']}" for n in items)
        news = f"\n## 📰 News\n\n{rows}\n"
    folds = m["folds"]
    skill = m.get("skill", m["name"])

    registry = load("registry.yml")
    reg_tables = grouped(
        registry, REG_CATS,
        lambda u: (f"| [`{u['repo']}`](https://github.com/{u['repo']}) | {u['why']} "
                   f"| {'⭐ ' + str(u['stars']) if u.get('stars') is not None else '—'} "
                   f"| {(u.get('pushed_at') or '—')[:10]} |"),
        "| Repo | Why tracked | Stars | Last push |\n|------|-------------|-------|-----------|")

    papers = grouped(
        load("papers.yml"), PAPER_CATS,
        lambda p: f"| [{p['title']}]({p['url']}) | {p['cite']} | {p['why']} |",
        "| Paper | Cite | Why it matters |\n|-------|------|----------------|")

    labs = grouped(
        load("labs.yml"), LAB_CATS,
        lambda l: (f"| [{l['name']}]({l['url']}) | {l['what']} | {l['why']} "
                   f"| {l['flagship']} |"),
        "| Org | What | Why it matters | Flagship |\n|-----|------|----------------|----------|")

    blogs = grouped(
        load("blogs.yml"), BLOG_CATS,
        lambda b: f"| {b['author']} | [{b['title']}]({b['url']}) | {b['year']} | {b['why']} |",
        "| Author | Post | Year | Why canonical |\n|--------|------|------|---------------|")

    people = grouped(
        load("people.yml"), PEOPLE_CATS,
        lambda p: (f"| [{p['name']}]({p['link']}) | {p['affiliation']} "
                   f"| {p['known_for']} | {p['why']} |"),
        "| Person | Affiliation | Known for | Why future-making |\n"
        "|--------|-------------|-----------|-------------------|")

    security = grouped(
        load("security.yml"), SEC_CATS,
        lambda s: f"| [{s['name']}]({s['url']}) | {s['what']} | {s['why']} |",
        "| Entry | What | Why it matters |\n|-------|------|----------------|")

    oec_entries = load("oec.yml")
    oec_entries.sort(key=lambda e: list(HORIZONS).index(e.get("horizon", "now")))
    oec = grouped(
        [{**e, "category": e["pillar"]} for e in oec_entries], OEC_PILLARS,
        lambda o: (f"| [{o['name']}]({o['url']}) | {o['origin']} "
                   f"| {HORIZONS.get(o['horizon'], o['horizon'])} | {o['what']} | {o['why']} |"),
        "| Entry | Origin | Horizon | What | Why still load-bearing |\n"
        "|-------|--------|---------|------|-------------------------|")

    return f"""<!-- GENERATED by scripts/build.py from data/*.yml — DO NOT HAND-EDIT. Edit data/ and run `make build`. -->

# {m['emoji']} {m['title']}

{badges}

*{m['tagline']}*

{m['description']}

**For:** {m['audience']}
{news}
## 🧭 Three folds, one closed loop

| Fold | Promise |
|------|---------|
| 📚 **Knowledge** | {folds['knowledge']} |
| 🛠️ **Tooling** | {folds['tooling']} |
| 🤝 **Community** | {folds['community']} |

Knowledge feeds tooling, tooling serves community, community grows knowledge —
one place to rely on for everything that matters in this domain.

## 🧠 The big picture: OEC — Observe → Evaluate → Control

Evaluation is the middle of a loop, not the whole of it. Three laws:

1. **Observability precedes eval** — you cannot evaluate what you cannot observe.
   Instrument first. (Kalman 1960 proved observability and controllability are
   mathematical duals — the O and the C were born twins.)
2. **Eval targets the objective, not just the engineering** — "is the code sound?"
   AND "is the business objective on track?", across the whole lifecycle:
   design → planning → execution → maintenance → upgrade. (Happy name collision:
   Kohavi's **OEC** — *Overall Evaluation Criterion* — is the canonical single
   business metric of A/B testing. Same letters, same spirit: the criterion IS
   the business objective.)
3. **Eval without control is a scoreboard** — after eval come decisions and change:
   gates, rollbacks, error budgets, kaizen. The loop must close.

This repo's loop maps onto OEC: `scope+collect+run` = **O** · `judge` = **E** ·
`gate+compound` = **C**. Below, the survival-tested canon of each pillar across
three horizons — 🏛️ 300 years (survived generations) · 🧭 30 years (survived the
hype cycle) · ⚡ now (rising, mid-2026):

{oec}

## 📡 Tracked upstream (the meta-repo)

Top-rated repos this repo tracks — refreshed weekly by `make sync`
(open GitHub API, human-gated PR with "what moved"):

{reg_tables}

## 📄 Seminal papers

Citation rigor: every entry links its **primary source** (paper/DOI), never the
trade article that covered it. Researched and web-verified 2026-07-22.

{papers}

## 🏛️ Labs & organizations

{labs}

## ✍️ Canonical blogs & blogposts

{blogs}

## 🌟 Ground-breaking & future-making people

Affiliations verified 2026-07-22 where possible — people move fast in this field;
uncertain affiliations are marked.

{people}

## 🛡️ Guardrails & security — the adversarial-eval fold

**Decision (2026-07-22):** security lives *inside* eval-anything — red-teaming IS
adversarial evaluation; the benchmarks, judges, and people overlap too heavily to
split. It spins out into a sibling repo only if this fold demonstrably outgrows
the measurement content. Security *repos* are tracked in the registry above;
standards, papers, tools, labs, and people live here.

{security}

## ⭐ The super-tool: `/{skill}`

One slash, no grammar, no expertise required. Say what you want — even vaguely —
and the skill infers intent from the bigger context (this repo's ledger, commits,
your history) before acting. Irreversible actions are always drafted for a human
to ship, never auto-executed. See `skills/{skill}/SKILL.md`.

## ♻️ The loop

`{arrow}`

| # | Stage | Promise (observable) |
|---|-------|----------------------|
{loop_rows}

Every promise above is **observable → eval-able → improve-able** — `make check` is the finish line.

## 👨‍👩‍👧‍👦 The repo family

| Repo | Relation |
|------|----------|
{fam_rows}

## 🧪 Verify

```bash
make check   # validate + tests + self-audit + drift gate — nothing ships red
```

## 📄 License

{m['license']} — see LICENSE.
"""


if __name__ == "__main__":
    out = ROOT / "README.md"
    text = render()
    if "--check" in sys.argv:
        if not out.exists() or out.read_text() != text:
            print("❌ drift: committed README.md ≠ generated (run `make build`)")
            sys.exit(1)
        print("✅ drift gate green")
    else:
        out.write_text(text)
        print(f"✅ wrote {out}")
