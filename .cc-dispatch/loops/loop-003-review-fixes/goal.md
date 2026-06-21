# Loop 003 — Apply four-source review fixes to CodeBlock.vue

**Repo:** `~/src/spantree/trellis-codeblock` · **Branch:** `main`
**Linear:** TRLS-43 · **Predecessor:** loop-002 (`dd0fd59`)

Four blind reviewers (CC, Codex, CodeRabbit, SonarQube) ran on `dd0fd59`.
SonarQube came back clean. The other three agreed on the fixes below.
Apply them in priority order, verify with the story slides, commit.

## Fixes (F1–F7)

### F1 — CRITICAL: Move highlighter to true module scope + expand language list

**Problem:** `highlighterPromise` is declared inside `<script setup>`, which Vue
compiles to a per-instance `setup()` function. Every CodeBlock creates its own
Shiki instance — the singleton comment is wrong. 12 slides = 12 Shiki inits.
Additionally, the hardcoded `langs` list (`typescript, python, go, yaml, bash,
shell`) will throw on any unlisted language (`json`, `tsx`, `javascript`, `html`,
`css`, `diff`, `text`, `sh`, `rust`, etc.), the rejection skips `calcFontSize`
AND the ResizeObserver setup, and the failed promise is cached → breaks every
subsequent CodeBlock on the deck.

**Fix:**
1. Add a regular `<script lang="ts">` block (above `<script setup>`) that declares
   `highlighterPromise` and `getHighlighter()` at module scope. This is the
   standard Vue 3 pattern for module-level state in SFCs.
2. Expand `langs` to cover what a 50-slide conference deck will realistically hit:
   ```
   typescript, javascript, tsx, jsx,
   python, go, rust, java, kotlin,
   yaml, json, toml,
   bash, shell, sh, zsh,
   html, css, vue,
   diff, text
   ```
3. Remove the `langs` / `themes` arrays from `<script setup>` — they belong only
   in the module-level `getHighlighter()`.

```html
<!-- module-level singleton — shared across ALL instances -->
<script lang="ts">
import { createHighlighter } from 'shiki'
import type { Highlighter } from 'shiki'
import setiTheme from '../themes/seti.json'

let highlighterPromise: Promise<Highlighter> | null = null

export function getHighlighter(): Promise<Highlighter> {
  if (!highlighterPromise) {
    highlighterPromise = createHighlighter({
      langs: [
        'typescript', 'javascript', 'tsx', 'jsx',
        'python', 'go', 'rust', 'java', 'kotlin',
        'yaml', 'json', 'toml',
        'bash', 'shell', 'sh', 'zsh',
        'html', 'css', 'vue',
        'diff', 'text',
      ],
      themes: [setiTheme as any, 'dracula', 'github-dark'],
    }).catch((err) => {
      highlighterPromise = null  // reset so next mount can retry
      throw err
    })
  }
  return highlighterPromise
}
</script>

<script setup lang="ts">
// Remove highlighterPromise and getHighlighter from here.
// Import getHighlighter from the module block above (same file, auto-available).
...
</script>
```

### F2 — MAJOR: try/catch in render() with fallback display

**Problem:** `render()` has no error handling. An unsupported lang/theme causes
`codeToHtml` to throw. The unhandled rejection in `onMounted` also skips the
`await nextTick()` + `calcFontSize()` + ResizeObserver attach sequence.

**Fix:** wrap the Shiki call in try/catch; on failure render an escaped plaintext
fallback (visible code, wrong colours — far better than a blank slide):

```typescript
async function render() {
  if (!props.code) {
    highlighted.value = ''
    return
  }
  try {
    const highlighter = await getHighlighter()
    highlighted.value = highlighter.codeToHtml(props.code, {
      lang: props.language!,
      theme: props.theme!,
    })
  } catch (err) {
    console.warn('[CodeBlock] Shiki render failed:', err)
    // Plaintext fallback — at least the code is readable
    highlighted.value = `<pre class="shiki shiki-fallback"><code>${escapeHtml(props.code)}</code></pre>`
  }
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}
```

Also: clear `highlighted.value = ''` before the early return when `!props.code`
(currently leaves stale HTML when code prop is cleared).

### F3 — MAJOR: Fix tab expansion in calcFontSize

**Problem:** `maxChars` uses `line.length`, counting `\t` as 1 character. CSS
`tab-size: 4` renders it as 4 columns. Tab-indented code (Go, many others) has
its font computed too large, silently overflowing `overflow: hidden`.

**Fix:** expand tabs before measuring. Also cache the metrics (lines + maxChars)
in a computed so resize storms don't rescan the string:

```typescript
// Cache — recomputed only when props.code changes
const codeMetrics = computed(() => {
  if (!props.code) return { numLines: 0, maxChars: 0 }
  const lines = props.code.split('\n')
  const expanded = lines.map(l => l.replace(/\t/g, '    '))  // tab = 4 cols
  return {
    numLines: lines.length,
    maxChars: Math.max(...expanded.map(l => l.length), 1),
  }
})
```

Use `codeMetrics.value.numLines` and `codeMetrics.value.maxChars` in `calcFontSize`.

### F4 — MAJOR: Add max font clamp + zero-container guard

**Problem:** Only an 8px floor, no ceiling. A 5-line `noChrome` slide computes an
enormous font size. Also, `calcFontSize` runs while Slidev mounts hidden slides
where `clientWidth/clientHeight` are 0, producing NaN/Infinity.

**Fix:**

```typescript
function calcFontSize() {
  const el = containerRef.value
  if (!el) return
  const w = el.clientWidth
  const h = el.clientHeight
  if (w <= 0 || h <= 0) return   // hidden/unmeasurable — wait for next resize

  const { numLines, maxChars } = codeMetrics.value
  if (numLines === 0 || maxChars === 0) return

  const chromeH = props.noChrome ? 0 : TITLEBAR_H
  const availW = Math.max(w - CODE_PAD_W, 1)
  const availH = Math.max(h - chromeH - CODE_PAD_H, 1)

  const byWidth = availW / (maxChars * CHAR_WIDTH_RATIO)
  const byHeight = availH / (numLines * LINE_HEIGHT)
  computedFontSize.value = Math.min(
    MAX_FONT_SIZE,                              // ceiling
    Math.max(MIN_FONT_SIZE, Math.floor(Math.min(byWidth, byHeight)))
  )
}

const MIN_FONT_SIZE = 8
const MAX_FONT_SIZE = 48   // 48px is readable at 1280px wide; adjust if needed
```

### F5 — MINOR: Await document.fonts.ready before first calcFontSize

**Problem:** `calcFontSize` can run before Fira Code has loaded, using fallback
monospace metrics. No resize event fires when the font loads, so the calculation
stays wrong.

**Fix:** in `onMounted`, await fonts before the first calc:

```typescript
onMounted(async () => {
  await render()
  await nextTick()
  await document.fonts.ready   // wait for Fira Code before measuring
  calcFontSize()
  ro = new ResizeObserver(calcFontSize)
  if (containerRef.value) ro.observe(containerRef.value)
})
```

### F6 — MINOR: Add `shiki` as an explicit devDependency

**Problem:** `shiki` is imported in `CodeBlock.vue` but only present as a
transitive dependency of `@slidev/cli`. This works in the monorepo but will break
if Slidev ever upgrades or inlines its Shiki dependency.

**Fix:**
```bash
bun add -d shiki
```

## Verification

After all fixes:

1. **`bun run build`** — exit 0
2. **Dev server up** — `curl -s http://localhost:3030/ | grep -c '<'` > 0
3. **Language coverage** — add a temporary slide using `json` and `html`; both must
   render with colour. Remove the temp slide before committing.
4. **Tab handling** — the Go story (slide 3) must not clip. Screenshot it and
   confirm all lines are visible at a readable font size.
5. **Font clamp** — the no-chrome story (slide 9, 5 lines) must not exceed 48px.
6. **Singleton** — open browser devtools on slide 1, type
   `window.__shikiSingletonTest = true` in console, navigate to slide 2, confirm
   no second `createHighlighter` call in the network tab or console.
7. **Fallback** — temporarily add an invalid `language="not-a-real-lang"` to any
   story slide; the fallback plaintext block must appear (not a blank slide).
   Remove before committing.

## Green gate

- `bun run build` exits 0
- All 12 original story slides render without errors
- Go story is unclipped
- No-chrome story font ≤ 48px
- JSON/HTML story slides render with colour
- Fallback renders on bad lang
- F6: `shiki` appears in `package.json` devDependencies

## Safety rules

- Do NOT touch the GOTO 2026 masterclass deck
- Do NOT change the `themes/seti.json` token colours (separate concern)
- The `code` prop API is frozen — do not change it
- Remove any temporary verification slides before committing

## Checkpoint

Write `report.md`, commit as `fix: apply four-source review fixes (F1-F6)`, notify, STOP.
