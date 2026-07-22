// Server-side view of the shared corpus — single source of truth is ../data.js,
// which is GENERATED from the repo's data/*.yml (drift-gated).
const { BRIEF_DATA } = require("../data.js");
module.exports = { CORPUS: BRIEF_DATA.corpus };
