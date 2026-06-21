# Loop 001 — CodeBlock component report

**Status:** ✅ Green gate met. Dev server live on port **3030**, all 12 story
slides render error-free, canonical Python/Seti slide matches Carbon's Seti output.

## Dev server

- **Local URL:** http://localhost:3030/
- **Port:** 3030 (started with `--remote` so the tailnet host can reach it)
- **Log:** `/tmp/trellis-codeblock.log`
- Started with:
  ```bash
  nohup bun run slidev slides.md --port 3030 --remote > /tmp/trellis-codeblock.log 2>&1 &
  ```

## ⚠️ ACTION REQUIRED — Cedric runs this

The `openclaw` agent user cannot bind the Tailscale daemon. The tailnet port is
already registered (via the tailscale skill); you just need to bind the serve:

```bash
/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --https=39738 http://localhost:3030
```

Once bound, the deck is live at:

- **Deck:** https://cedrics-mac-mini-2.tailb5984b.ts.net:39738
- **Presenter:** https://cedrics-mac-mini-2.tailb5984b.ts.net:39738/presenter/1

| Field | Value |
|-------|-------|
| Tailnet host | `cedrics-mac-mini-2.tailb5984b.ts.net` |
| Tailnet port | `39738` |
| Local port | `3030` |
| Service name | `slides` |

## Per-phase notes

### Phase A — setup
- `package.json` pinned `@slidev/cli@^0.51.0`, **which does not exist** — Slidev
  dropped the leading `0.` from its version scheme. No stable `0.51.x` ships
  (only `0.51.0-beta.x`). Installed the closest stable line, **`52.16.0`**
  (≈ the old `0.52`), which ships **`shiki@4.2.0`** as required.
- Added `@slidev/theme-default` + `@slidev/theme-seriph` — the default theme is
  not bundled with the CLI in this version and the server refused to start
  without it.
- `vite.config.ts` (`allowedHosts: true`) left untouched for Tailscale.

### Phase B — `CodeBlock.vue`
- Props per spec: `code`, `language`, `theme` (default `Seti`), `title`,
  `noChrome`, `fontSize`.
- Seti loaded as the custom JSON theme object from `themes/seti.json`
  (`theme: 'Seti'` matches its `name` field). `dracula` + `github-dark` come
  from Shiki's bundled set. **Never** used `theme: 'seti'` as a string.
- One shared highlighter promise across all instances (Shiki is expensive to
  init); `v-html` renders Shiki's `<pre class="shiki">`, restyled to use
  Fira Code at the requested size.
- Chrome is pure CSS: gradient canvas, 10px window radius,
  `0 20px 68px rgba(0,0,0,.55)` shadow, 28px titlebar, 12px traffic lights
  (#FF5F57 / #FEBC2E / #28C840), centered translucent title.

### Phase C — story slides
- 12 stories in `slides.md`, all using real, meaningful code.
- **Key fix:** multi-line backtick template literals inside Vue attributes
  (`:code="\`...\`"`) break the Vue template compiler ("Unterminated string
  constant") and markdown mangles the backticks. Solution: each snippet lives in
  `snippets/` and is imported with Vite's **`?raw`** — the file content *is* the
  displayed code, with zero escaping.
- Slidev scopes a markdown `<script setup>` block to **its own slide only**, not
  globally, so each slide carries its own import block.

### Phase D — Tailscale
- Port registered with the tailscale skill (`ensure --service slides
  --local-port 3030`) → tailnet port `39738`. Bind command above is Cedric's to
  run (daemon access).

## Verification (headless Chromium, 1920×1080)

- All 12 stories: `<pre class="shiki">` present, **0 console/page errors**.
- Canonical Python/Seti token colors sampled from the live DOM:
  - keywords (`def`/`class`/`async`/`import`/`return`) → `#e6cd69` (yellow) ✓
  - strings → `#55b5db` (blue) ✓
  - operators (`=`, `*`) / params (`self`, `prompt`) → `#9fca56` (green) ✓
  - class/type names (`Agent`) → `#a074c4` (purple) ✓
  - numbers / `None` → `#cd3f45` (red) ✓
  - foreground / punctuation → `#CFD2D1` ✓
- Fira Code confirmed (the `->` ligature renders as `→` in the screenshot).

## Commits

1. `chore: install Slidev 52.16.0 (Shiki v4.2.0)`
2. `feat: add CodeBlock.vue with Seti theme + 12 story slides`
