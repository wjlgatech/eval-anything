// Vercel serverless function: site copilot grounded in the eval-anything corpus.
// Requires ANTHROPIC_API_KEY in the Vercel project env. Without it, returns 503 and
// the client falls back to labeled offline retrieval — it never fakes an LLM answer.
// Pattern: graph-engineering-anything brief/api/chat.js (family reference).
const { CORPUS } = require("./_corpus.js");

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) return res.status(503).json({ error: "no ANTHROPIC_API_KEY configured" });

  const { question } = req.body || {};
  if (!question || typeof question !== "string" || question.length > 2000)
    return res.status(400).json({ error: "bad question" });

  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": key,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-5",
      max_tokens: 700,
      system:
        "You are the copilot for eval-anything — the Evaluation Operating System " +
        "(OEC: Observe → Evaluate → Control; benchmarks, harnesses, LLM-as-judge, guardrails/security; " +
        "a weekly-synced registry; an /eval-anything super-tool). " +
        "Answer ONLY from the corpus below. Preserve caveats when citing (saturation, contamination status, " +
        "judge biases, 'unverified' flags). If the corpus doesn't cover the question, " +
        "say so plainly — never invent a number, benchmark, repo, or source.\n\n=== CORPUS ===\n" +
        CORPUS.join("\n\n"),
      messages: [{ role: "user", content: question }],
    }),
  });

  if (!r.ok) {
    const detail = await r.text().catch(() => "");
    return res.status(502).json({ error: "upstream " + r.status, detail: detail.slice(0, 300) });
  }
  const j = await r.json();
  const answer = (j.content || []).filter(b => b.type === "text").map(b => b.text).join("\n") || "(empty response)";
  res.status(200).json({ answer });
};
