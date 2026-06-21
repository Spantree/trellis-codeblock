---
title: Fix CodeBlock layout — light bg, no canvas, auto font, no overflow
linear_url: https://linear.app/spantree/issue/TRLS-43
last_updated: 2026-06-20T21:08:00-05:00
---

# Loop 002 — Fix CodeBlock layout: light bg, no canvas, auto font, no overflow

**Repo:** `~/src/spantree/trellis-codeblock` · **Branch:** `main` directly
**Mode:** autonomous. **Linear:** TRLS-43.

## Feedback from Cedric (loop-001 review)

1. **Slide background should be light** — slides are rendering dark (black bg from Seti theme bleeding through). The slide canvas itself should be white/light; only the CodeBlock window is dark.
2. **Remove the grey canvas** — strip the outer `linear-gradient(135deg, #c0c5cc…)` wrapper entirely. The dark window renders directly on the light slide background. No outer container, no padding, no shadow on the slide itself.
3. **Fixed size + auto font** — The CodeBlock window should be a fixed size (container-relative, like `contained-video` in the GOTO deck). The font auto-scales to fill the most constrained dimension (width or height). If code doesn't fill perfectly, the remainder is whitespace.
4. **No overflow** — slides 2, 4, 7, 8, 11, 12 currently overflow. Font must shrink to fit rather than overflow.
5. **Equal-height two-column** — both code blocks in the two-column slide must have the same number of lines. Pad the shorter snippet with trailing empty lines to match the taller one.

---

## Phase A — Light slide background

In `slides.md` headmatter (the very first `---` block), add or update:

```yaml
colorSchema: light
background: '#ffffff'
```

This forces the Slidev canvas to be white/light for all slides. Verify that the CodeBlock's dark window still renders correctly on a light background — it should, since the window has its own dark `background: #151718`.

---

## Phase B — Remove the canvas, fill the slide

**Remove from `CodeBlock.vue`:**
- The entire `.codeblock-canvas` div and its CSS (the gradient wrapper + 56px padding)
- The `.codeblock-canvas` CSS class entirely

**Replace with a fill container:**

The template root becomes:

```html
<template>
  <div ref="containerRef" class="codeblock-fill">
    <div class="codeblock-window">
      <!-- titlebar + code unchanged -->
    </div>
  </div>
</template>
```

`.codeblock-fill`:
```css
.codeblock-fill {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

`.codeblock-window` — keep existing styles (border-radius, box-shadow, background) but remove `min-width: 320px` and add:
```css
.codeblock-window {
  /* fills horizontally, lets font-size drive height */
  width: 100%;
}
```

---

## Phase C — Auto font size

Remove the `fontSize` prop (or keep as a manual override but stop using it as the default path). Auto-calculate the optimal font size from container dimensions and code metrics.

**Add to `<script setup>`:**

```typescript
import { onMounted, onUnmounted, ref, watch, nextTick } from 'vue'

const containerRef = ref<HTMLElement | null>(null)
const computedFontSize = ref(16)

const CHAR_WIDTH_RATIO = 0.603   // Fira Code: char width ≈ 0.603 × fontSize
const LINE_HEIGHT      = 1.45
const CODE_PAD_H       = 48      // 24px top + 24px bottom padding on .codeblock-code
const CODE_PAD_W       = 64      // 32px left + 32px right
const TITLEBAR_H       = 28      // when chrome is visible

function calcFontSize() {
  const el = containerRef.value
  if (!el || !props.code) return
  const w = el.clientWidth
  const h = el.clientHeight

  const lines    = props.code.split('\n')
  const numLines = lines.length
  const maxChars = Math.max(...lines.map(l => l.length), 1)

  // Available area after chrome and padding
  const chromeH = props.noChrome ? 0 : TITLEBAR_H
  const availW  = w - CODE_PAD_W
  const availH  = h - chromeH - CODE_PAD_H

  // Font that fits width vs font that fits height — take the smaller
  const byWidth  = availW  / (maxChars * CHAR_WIDTH_RATIO)
  const byHeight = availH  / (numLines * LINE_HEIGHT)
  computedFontSize.value = Math.max(8, Math.floor(Math.min(byWidth, byHeight)))
}

let ro: ResizeObserver | null = null
onMounted(async () => {
  await nextTick()
  calcFontSize()
  ro = new ResizeObserver(calcFontSize)
  if (containerRef.value) ro.observe(containerRef.value)
})
onUnmounted(() => ro?.disconnect())
watch(() => [props.code, props.language, props.noChrome], async () => {
  await nextTick()
  calcFontSize()
})
```

**In the template**, bind the font size to the `.codeblock-code` div:

```html
<div class="codeblock-code" :style="{ fontSize: computedFontSize + 'px' }">
```

**In CSS**, change overflow on `.codeblock-code` and `pre.shiki`:

```css
.codeblock-code {
  overflow: hidden;   /* was overflow-x: auto — no scrollbars, font fits */
}
.codeblock-code :deep(pre.shiki) {
  overflow: hidden;   /* same */
  white-space: pre;
}
```

---

## Phase D — Equal-height two-column

In the story slide for **slide 12 (two-column)**, both snippets must have the same number of lines. Before passing to `:code`, pad the shorter one with trailing `\n` to match:

```typescript
// In slide 12's <script setup>
const maxLines = Math.max(
  codeA.split('\n').length,
  codeB.split('\n').length,
)
const padA = codeA + '\n'.repeat(Math.max(0, maxLines - codeA.split('\n').length))
const padB = codeB + '\n'.repeat(Math.max(0, maxLines - codeB.split('\n').length))
```

Then pass `padA` and `padB` to the two `<CodeBlock>` instances.

---

## Phase E — Story slide layout fix

The story slides need to give `CodeBlock` something to fill. With the canvas removed, the component needs the slide's content area to be sized. Update each story slide to use a layout that fills available space.

Add a `codeblock-slide` CSS class to `slides.md`'s global styles (or `style.css` if one exists):

```css
.codeblock-slide {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 48px;
  box-sizing: border-box;
}
.codeblock-slide .cb-wrapper {
  flex: 1 1 0;
  min-height: 0;
}
```

Each story slide's body:

```html
<div class="codeblock-slide">
  <h2>Story title</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" :code="code" />
  </div>
</div>
```

For the two-column slide, side by side in `.cb-wrapper`:

```html
<div class="cb-wrapper" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
  <CodeBlock ... :code="padA" />
  <CodeBlock ... :code="padB" />
</div>
```

---

## Verification

After changes, visually confirm:
1. All slides have a **white/light background** — the Seti dark window floats on white
2. **No grey canvas** around the code window
3. **No overflow** on any of the 12 slides
4. Font is **visibly larger** on short/simple slides (5-line code fills more space) and **visibly smaller** on long/dense slides
5. **Slide 12 (two-column)**: both panels same height, same line count
6. Screenshot the canonical Python/Seti slide and compare to the kermit Carbon export — same colors, similar feel, white background

Restart the dev server after changes: `kill` the running server and re-run `bun run slidev slides.md --port 3030 --remote`.

## Green gate

1. `bun run build` — exit 0
2. All 12 slides: white background, no overflow, no canvas
3. Font visibly auto-scales across slides
4. Two-column equal height

## Checkpoint

Write `report.md`, notify, STOP. Include screenshots of at least slides 1, 7, and 12.
