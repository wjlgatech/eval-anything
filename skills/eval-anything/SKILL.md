---
name: eval-anything
description: Turn any "is it good enough / safe enough / on track?" question into a gated eval — pick the right benchmark or harness for a model/agent, design an eval with maker≠checker judging and bias checks, red-team guardrails, wire the OEC loop (observability before eval, control after eval, business objective as the criterion), or track what moved in the eval field this week. Accepts vague prompts — no grammar or expertise required; infers intent from context before acting. Trigger: "/eval-anything", "eval this model", "eval this agent", "which benchmark", "design an eval", "red-team this", "LLM-as-judge", "is this objective on track", "what should we observe", "how do we act on eval results". NOT for: general ML training questions with no measurement claim; human HR-style performance reviews.
---

# /eval-anything — the super-tool

The front door for `wjlgatech/eval-anything`. One slash away; designed to be
**easy to use and hard to misuse**.

## The super-tool contract (non-negotiable)

1. **No grammar, no expertise required.** Accept vague prompts as first-class input.
2. **Infer intent from the bigger context before asking.** Read, in order: this
   repo's ledger (`data/news.yml`), recent `git log`, the current session, and any
   longitudinal history available. Reflect the inferred intent back in ONE line
   before any non-trivial action.
3. **≤1 clarifying question, and only at a real fork.** When intent confidence is
   low, ask exactly one question; when proceeding on an assumption, state it —
   never silently fill a gap.
4. **Hard to misuse.** Irreversible/outward actions (publish, post, delete, pay,
   push) are ALWAYS drafted-then-human-shipped. An honest ❌ beats a fake ✅.

## Backbone (always on)

| User wants… | Do |
|---|---|
| design any eval | walk the OEC loop: what can we OBSERVE (instrument first)? what CRITERION says the objective — engineering AND business — is on track? what CONTROL acts on the verdict (gate/rollback/change)? An eval with no control hook is a scoreboard — flag it |
| observe an agent run (O before E) | `make observe` (this project's sessions) · `scripts/observe.py --json|--eval` for machine/eval consumption · `npx agent-flow-app` for the live human view (same ground truth) |
| verify the repo | `make check` — the only truth |
| what's new / what moved | the 📰 News section + `make sync` (weekly heartbeat) |
| learn the domain | the 📚 Knowledge fold — README registry, one reliable place |
| regenerate artifacts | `make build` (never hand-edit generated files) |
| contribute | add one row to the registry, open a PR (Community fold) |

## Progressive disclosure

Load deeper references only on trigger — keep the backbone lean
(FM-os hub / longevity-loop SKILL.md pattern).
