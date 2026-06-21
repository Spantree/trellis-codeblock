---
theme: default
title: CodeBlock Story Slides
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
layout: center
---

<script setup lang="ts">
import raw from './snippets/01-agent.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 1 · Python / Seti / Medium

<CodeBlock language="python" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/02-debounce.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 2 · TypeScript / Seti / Short

<CodeBlock language="typescript" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/03-worker.go?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 3 · Go / Seti / Medium

<CodeBlock language="go" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/04-deploy.yaml?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 4 · YAML / Seti / Short

<CodeBlock language="yaml" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/05-serve.sh?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 5 · Bash / Seti / Short

<CodeBlock language="bash" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/06-cache.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 6 · Python / Dracula / Medium

<CodeBlock language="python" theme="dracula" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/07-users.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 7 · TypeScript / GitHub Dark / Medium

<CodeBlock language="typescript" theme="github-dark" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/08-anthropic.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 8 · With title bar

<CodeBlock language="python" title="agent.py" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/09-greet.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 9 · No chrome

<CodeBlock language="python" :noChrome="true" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/10-pipeline.py?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 10 · Long lines (horizontal overflow)

<CodeBlock language="python" title="pipeline.py" :code="code" />

---
layout: center
---

<script setup lang="ts">
import raw from './snippets/11-store.ts?raw'
const code = raw.replace(/\n+$/, '')
</script>

# 11 · Long code (vertical fill)

<CodeBlock language="typescript" :fontSize="13" title="store.ts" :code="code" />

---
layout: default
---

<script setup lang="ts">
import rawA from './snippets/12a-retry.ts?raw'
import rawB from './snippets/12b-usage.ts?raw'
const codeA = rawA.replace(/\n+$/, '')
const codeB = rawB.replace(/\n+$/, '')
</script>

# 12 · Two-column — definition + usage

<div class="grid grid-cols-2 gap-4 mt-4">

<CodeBlock language="typescript" :fontSize="12" title="retry.ts" :code="codeA" />

<CodeBlock language="typescript" :fontSize="12" title="usage.ts" :code="codeB" />

</div>
