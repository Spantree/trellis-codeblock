---
theme: default
title: CodeBlock Story Slides
colorSchema: light
background: '#ffffff'
fonts:
  mono: Fira Code
---

# CodeBlock — Story Slides

A Slidev project for developing the `CodeBlock` Vue component.
Carbon-style macOS chrome + custom **Seti** Shiki theme.

Each slide demonstrates one combination of language, theme, length, and chrome.
Snippets are imported raw (Vite `?raw`) so the file content *is* the displayed code —
zero escaping, no markdown/attribute interference.

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/01-agent.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>1 · Python / Seti / Medium</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/02-debounce.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>2 · TypeScript / Seti / Short</h2>
  <div class="cb-wrapper">
    <CodeBlock language="typescript" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/03-worker.go?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>3 · Go / Seti / Medium</h2>
  <div class="cb-wrapper">
    <CodeBlock language="go" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/04-deploy.yaml?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>4 · YAML / Seti / Short</h2>
  <div class="cb-wrapper">
    <CodeBlock language="yaml" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/05-serve.sh?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>5 · Bash / Seti / Short</h2>
  <div class="cb-wrapper">
    <CodeBlock language="bash" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/06-cache.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>6 · Python / Dracula / Medium</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" theme="dracula" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/07-users.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>7 · TypeScript / GitHub Dark / Medium</h2>
  <div class="cb-wrapper">
    <CodeBlock language="typescript" theme="github-dark" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/08-anthropic.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>8 · With title bar</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" title="agent.py" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/09-greet.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>9 · No chrome</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" :noChrome="true" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/10-pipeline.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>10 · Long lines (auto-shrink to fit width)</h2>
  <div class="cb-wrapper">
    <CodeBlock language="python" title="pipeline.py" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import raw from './snippets/11-store.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

<div class="codeblock-slide">
  <h2>11 · Long code (auto-shrink to fit height)</h2>
  <div class="cb-wrapper">
    <CodeBlock language="typescript" title="store.ts" :code="code" />
  </div>
</div>

---
layout: default
---

<script setup lang="ts">
import rawA from './snippets/12a-retry.ts?raw'
import rawB from './snippets/12b-usage.ts?raw'
const codeA = rawA.replace(/\n+$/, '')
const codeB = rawB.replace(/\n+$/, '')
const maxLines = Math.max(codeA.split('\n').length, codeB.split('\n').length)
const padA = codeA + '\n'.repeat(Math.max(0, maxLines - codeA.split('\n').length))
const padB = codeB + '\n'.repeat(Math.max(0, maxLines - codeB.split('\n').length))
</script>

<div class="codeblock-slide">
  <h2>12 · Two-column — definition + usage</h2>
  <div class="cb-wrapper" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
    <CodeBlock language="typescript" title="retry.ts" :code="padA" />
    <CodeBlock language="typescript" title="usage.ts" :code="padB" />
  </div>
</div>
