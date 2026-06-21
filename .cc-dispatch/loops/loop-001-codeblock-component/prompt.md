Build a CodeBlock.vue Slidev component with custom Seti syntax theme and Carbon-style macOS chrome,
then expose the dev server over Tailscale serve.

READ FIRST:
- `goal.md` (repo root) — full spec: phases, green-gate, Shiki v4 notes, safety rules.
- `themes/seti.json` — the custom Seti theme (already committed). Do NOT use `theme: 'seti'` as a string; it is not bundled in Shiki v4.

Mode: autonomous (--dangerously-skip-permissions). Work directly on `main`.
Do NOT touch any other repo or the GOTO 2026 masterclass deck.

Done when: dev server is running on port 3030, all 12 story slides render without error,
the canonical Python/Seti/Medium story visually matches Carbon's Seti output (correct colors,
traffic lights, Fira Code font), and `report.md` is written with the dev server port + the
`tailscale serve` command Cedric needs to run to bind it — or stop after 40 turns and report what's blocking.

Stop after the gate passes: write `report.md`, commit, notify. Do not begin Phase E (Trellis port) or any unrelated work.
