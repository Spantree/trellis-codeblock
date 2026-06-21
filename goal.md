# Loop 001 — Build CodeBlock component with Seti theme and Carbon chrome

**Repo:** `~/src/spantree/trellis-codeblock` · **Branch:** `main` directly  
**Mode:** autonomous. **Linear:** [TRLS-43](https://linear.app/spantree/issue/TRLS-43/build-codeblock-component-with-seti-theme-and-carbon-chrome).

## Context

This is a toy Slidev project (`trellis-codeblock`) for developing and previewing a `CodeBlock` Vue component before it gets ported into the GOTO 2026 masterclass deck and eventually the core Trellis library.

The goal: a Vue component that makes code look as good as a Carbon ([carbon.now.sh](http://carbon.now.sh)) export — specifically the **Seti theme with macOS window chrome** — using Shiki for syntax highlighting and pure CSS for the carbon-style chrome. No PNG generation, no external API calls, no CodeMirror. Just a well-crafted Vue component.

## Target aesthetic

Reference: https://carbon.now.sh/?bg=rgba%28171%2C184%2C195%2C1%29&t=seti&wt=none&l=python&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Fira+Code&fs=14px&lh=143%25

The output should match Carbon's Seti theme closely:

**Canvas / outer wrapper:**
- Light gray/cream gradient background (`linear-gradient(135deg, #c0c5cc 0%, #b3bac2 100%)` or similar)
- Generous padding around the code window (56px matches Carbon's default)
- Drop shadow under the window: `0 20px 68px rgba(0,0,0,0.55)` (Carbon uses a pronounced shadow)
- Border radius on the window: `10px` (mac window radius)

**Window chrome (title bar):**
- Dark background: `#282a36` or `#1c1c1c` (slightly lighter than code area)
- Height: ~28px
- Three traffic-light dots, left-aligned with ~8px gap from left edge:
  - Red: `#FF5F57` (diameter ~12px)
  - Yellow: `#FEBC2E`
  - Green: `#28C840`
  - 6px gap between dots
- Optional title label: centered in the title bar, `color: rgba(255,255,255,0.4)`, `font-size: 12px`, `font-family: 'Fira Code', monospace`

**Code area:**
- Background: `#151718` (Seti's background color)
- Padding: `24px 32px`
- Font: `Fira Code` (import from Google Fonts if not locally available)
- Font size: 14px
- Line height: 1.45
- Color: Seti's default foreground (`#CFD2D1`)
- No scrollbars visible (overflow hidden or custom-styled)
- No cursor
- Syntax token colors match Seti (loaded from `themes/seti.json` — authoritative colors from Carbon's `constants.js`)

## Seti theme — important notes

**`seti` is NOT a bundled theme in Shiki v4.** Do not use `theme: 'seti'` — it will fail at runtime.

The canonical Seti theme JSON is already in the repo at `themes/seti.json`. Load it as a custom theme:

```typescript
import { createHighlighter } from 'shiki'
import setiTheme from '../themes/seti.json'

// In setup():
const highlighter = await createHighlighter({
  langs: ['typescript', 'python', 'go', 'yaml', 'bash', 'shell'],
  themes: [setiTheme],
})

const html = highlighter.codeToHtml(code, {
  lang: props.language ?? 'typescript',
  theme: 'Seti',  // must match the "name" field in themes/seti.json
})
```

For alternate themes in story slides (dracula, github-dark), those ARE bundled in Shiki v4 — add them to the `themes` array in `createHighlighter`.

## Phase A — Project setup

**Install dependencies and configure Slidev:**

```bash
cd ~/src/spantree/trellis-codeblock
bun install  # installs @slidev/cli v0.51, @slidev/types, vue
```

If `bun install` fails on v0.51, try `bun add @slidev/cli @slidev/types vue` without pinning the exact version — use whatever stable v0.51.x is available.

Add Fira Code font: In `slides.md` headmatter, add:

```yaml
fonts:
  mono: Fira Code
```

This tells Slidev to pull Fira Code from Google Fonts automatically.

**`vite.config.ts` already exists** in the repo root with `allowedHosts: true` — needed for Tailscale serve. Do not remove it.

**Do NOT install shiki separately** — Slidev already includes it. Import from `shiki` (Slidev 0.51 ships with `shiki@^4.2.0`).

## Phase B — `CodeBlock.vue`

Create `components/CodeBlock.vue`. This is a Slidev auto-imported component — available in any slide by just using `<CodeBlock />`.

**Props:**

```typescript
interface Props {
  code: string           // required — raw code string to highlight
  language?: string      // default: 'typescript'
  theme?: string         // default: 'Seti' — must be in highlighter's themes list
  title?: string         // optional window title bar label
  noChrome?: boolean     // default: false — if true, hides title bar (keeps canvas + window bg)
  fontSize?: number      // px, default: 14
}
```

**Use the `code` prop directly** — do not attempt slot text extraction. Slidev pre-processes markdown code fences, making raw slot content unreliable. The `code` prop is the clean, ergonomic API for story slides.

**Template structure:**

```html
<div class="codeblock-canvas">
  <div class="codeblock-window">
    <div v-if="!noChrome" class="codeblock-titlebar">
      <div class="codeblock-dots">
        <span class="dot dot-red" />
        <span class="dot dot-yellow" />
        <span class="dot dot-green" />
      </div>
      <span v-if="title" class="codeblock-title">{{ title }}</span>
    </div>
    <div class="codeblock-code" v-html="highlighted" />
  </div>
</div>
```

**Script (setup):**

```typescript
import { createHighlighter } from 'shiki'
import type { Highlighter } from 'shiki'
import setiTheme from '../themes/seti.json'
// Import bundled themes used by story slides:
// 'dracula' and 'github-dark' are bundled in Shiki v4 — add as-is

const props = withDefaults(defineProps<Props>(), {
  language: 'typescript',
  theme: 'Seti',
  noChrome: false,
  fontSize: 14,
})

const highlighted = ref<string>('')

let highlighter: Highlighter | null = null

onMounted(async () => {
  highlighter = await createHighlighter({
    langs: ['typescript', 'python', 'go', 'yaml', 'bash', 'shell'],
    themes: [setiTheme, 'dracula', 'github-dark'],
  })
  await render()
})

watch(() => [props.code, props.language, props.theme], render)

async function render() {
  if (!highlighter || !props.code) return
  highlighted.value = highlighter.codeToHtml(props.code, {
    lang: props.language!,
    theme: props.theme!,
  })
}
```

**Note on Shiki's HTML output:** `codeToHtml` returns a `<pre><code>...</code></pre>` block with inline styles. Wrap it in `v-html` as shown — no sanitization needed in this controlled Slidev context.

## Phase C — Story slides

Replace `slides.md` with a comprehensive set of story slides. Each slide demonstrates one combination of props. Use the layouts Slidev ships with (`default`, `center`) — no custom layout needed here.

**Required stories:**

1. **Python / Seti / Medium (15 lines)** — the canonical story. Real Python code, meaningful snippet.
2. **TypeScript / Seti / Short (5 lines)** — simple TS function
3. **Go / Seti / Medium (15 lines)**
4. **YAML / Seti / Short (5 lines)** — config file
5. **Bash / Seti / Short (8 lines)** — shell script
6. **Python / Dracula / Medium** — alternate theme (`theme="dracula"`)
7. **TypeScript / GitHub Dark / Medium** — alternate theme (`theme="github-dark"`)
8. **With title bar** — Python / Seti / `title="agent.py"`
9. **No chrome** — Python / Seti / `noChrome` prop (hides title bar, keeps canvas gradient + window bg)
10. **Long lines (100+ chars)** — tests overflow behavior. Use `overflow: auto` horizontally in `.codeblock-code` so scroll works but doesn't look broken.
11. **Long code (30 lines)** — tests vertical fill at 1920×1080 slide canvas
12. **Two-column** — two `<CodeBlock>` side by side on one slide, showing related snippets (left: function definition, right: usage example)

Use **real, meaningful code** in every story — not `console.log("hello world")`. The stories should look like slides you'd actually show at a conference.

## Phase D — Expose via Tailscale serve

**No build/deploy step needed** — run the Slidev dev server locally and expose it over the tailnet.

```bash
# 1. Start dev server on a fixed local port
cd ~/src/spantree/trellis-codeblock
nohup bun run dev -- --port 3030 --remote > /tmp/trellis-codeblock.log 2>&1 &
sleep 8

# 2. Verify it's up
curl -s --max-time 5 http://localhost:3030/ | grep -c '<' || echo "WARN: server may still be starting"

# 3. Allocate a stable tailnet port via the Tailscale skill CLI
RESULT=$(bun run ~/.openclaw/workspace/skills/tailscale/cli.ts ensure \
  --cwd ~/src/spantree/trellis-codeblock \
  --service slides \
  --local-port 3030)
echo "$RESULT"
TAILNET_URL=$(echo "$RESULT" | jq -r .url)
TAILNET_PORT=$(echo "$RESULT" | jq -r .tailnetPort)

# 4. Output the serve command for Cedric to run (openclaw user can't bind the Tailscale daemon)
echo ""
echo "=== ACTION REQUIRED FOR CEDRIC ==="
echo "Run this in your terminal to bind Tailscale serve:"
echo "/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --https=${TAILNET_PORT} http://localhost:3030"
echo ""
echo "Deck will be live at: ${TAILNET_URL}"
```

**Important:** The `openclaw` agent user cannot communicate with the Tailscale daemon. CC can start the dev server and register the port, but Cedric must run the `tailscale serve` bind command himself in his own terminal session. Output the full command clearly in `report.md`.

## Green gate

1. `bun install` — exit 0
2. Dev server running on port 3030 (`curl http://localhost:3030/` returns HTML)
3. All 12 story slides render without errors in the browser
4. The canonical story (Python / Seti / Medium) visually matches Carbon's Seti output — dark window, traffic lights, Fira Code, correct yellow keywords / green operators / blue strings / purple types
5. `report.md` written with: tailnet URL, tailscale serve command for Cedric, per-phase notes

## Safety rules

- Do NOT modify the GOTO 2026 masterclass deck — this is a standalone toy project
- Do NOT use `theme: 'seti'` as a string — it's not bundled. Always use the JSON object from `themes/seti.json`
- If `createHighlighter` import fails, try `import { createHighlighter } from '@shikijs/core'` — same package, different entry
- Commit after each phase: setup, component, stories, server-up

## Checkpoint

Write `report.md`, notify, STOP. Include: dev server port, tailnet URL, tailscale serve command.
