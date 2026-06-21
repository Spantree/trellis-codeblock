<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, nextTick } from 'vue'
import { createHighlighter } from 'shiki'
import type { Highlighter } from 'shiki'
import setiTheme from '../themes/seti.json'

interface Props {
  code: string
  language?: string
  theme?: string
  title?: string
  noChrome?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  language: 'typescript',
  theme: 'Seti',
  noChrome: false,
})

const highlighted = ref<string>('')

// One shared highlighter across all CodeBlock instances on the deck.
let highlighterPromise: Promise<Highlighter> | null = null

function getHighlighter(): Promise<Highlighter> {
  if (!highlighterPromise) {
    highlighterPromise = createHighlighter({
      langs: ['typescript', 'python', 'go', 'yaml', 'bash', 'shell'],
      // 'Seti' is the custom JSON theme; dracula + github-dark are bundled in Shiki v4.
      themes: [setiTheme as any, 'dracula', 'github-dark'],
    })
  }
  return highlighterPromise
}

async function render() {
  if (!props.code) return
  const highlighter = await getHighlighter()
  highlighted.value = highlighter.codeToHtml(props.code, {
    lang: props.language!,
    theme: props.theme!,
  })
}

// --- Auto font size ----------------------------------------------------------
const containerRef = ref<HTMLElement | null>(null)
const computedFontSize = ref(16)

const CHAR_WIDTH_RATIO = 0.603 // Fira Code: char width ≈ 0.603 × fontSize
const LINE_HEIGHT = 1.45
const CODE_PAD_H = 48 // 24px top + 24px bottom on .codeblock-code
const CODE_PAD_W = 64 // 32px left + 32px right
const TITLEBAR_H = 28 // when chrome is visible

function calcFontSize() {
  const el = containerRef.value
  if (!el || !props.code) return
  const w = el.clientWidth
  const h = el.clientHeight

  const lines = props.code.split('\n')
  const numLines = lines.length
  const maxChars = Math.max(...lines.map((l) => l.length), 1)

  const chromeH = props.noChrome ? 0 : TITLEBAR_H
  const availW = w - CODE_PAD_W
  const availH = h - chromeH - CODE_PAD_H

  // Font that fits width vs font that fits height — take the smaller.
  const byWidth = availW / (maxChars * CHAR_WIDTH_RATIO)
  const byHeight = availH / (numLines * LINE_HEIGHT)
  computedFontSize.value = Math.max(8, Math.floor(Math.min(byWidth, byHeight)))
}

let ro: ResizeObserver | null = null

onMounted(async () => {
  await render()
  await nextTick()
  calcFontSize()
  ro = new ResizeObserver(calcFontSize)
  if (containerRef.value) ro.observe(containerRef.value)
})

onUnmounted(() => ro?.disconnect())

watch(() => [props.code, props.language, props.theme], render)
watch(() => [props.code, props.language, props.noChrome], async () => {
  await nextTick()
  calcFontSize()
})
</script>

<template>
  <div ref="containerRef" class="codeblock-fill">
    <div class="codeblock-window">
      <div v-if="!noChrome" class="codeblock-titlebar">
        <div class="codeblock-dots">
          <span class="dot dot-red" />
          <span class="dot dot-yellow" />
          <span class="dot dot-green" />
        </div>
        <span v-if="title" class="codeblock-title">{{ title }}</span>
      </div>
      <div
        class="codeblock-code"
        :style="{ fontSize: computedFontSize + 'px' }"
        v-html="highlighted"
      />
    </div>
  </div>
</template>

<style scoped>
.codeblock-fill {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.codeblock-window {
  /* Fixed-size window: fills the container; font-size fills the interior,
     any remainder is whitespace (Carbon "contained" feel). */
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  overflow: hidden;
  /* Pronounced Carbon-style drop shadow */
  box-shadow: 0 20px 68px rgba(0, 0, 0, 0.55);
  background: #151718;
}

.codeblock-titlebar {
  position: relative;
  flex: 0 0 28px;
  height: 28px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  background: #1c1c1c;
}

.codeblock-dots {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.dot-red {
  background: #ff5f57;
}

.dot-yellow {
  background: #febc2e;
}

.dot-green {
  background: #28c840;
}

.codeblock-title {
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
  pointer-events: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
  font-family: 'Fira Code', monospace;
}

.codeblock-code {
  flex: 1 1 0;
  min-height: 0;
  background: #151718;
  padding: 24px 32px;
  overflow: hidden;
}

/* Reset Shiki's emitted <pre>/<code> to inherit our typography */
.codeblock-code :deep(pre.shiki) {
  margin: 0;
  padding: 0;
  background: transparent !important;
  overflow: hidden;
  white-space: pre;
}

.codeblock-code :deep(code) {
  font-family: 'Fira Code', 'Fira Mono', monospace;
  font-size: inherit;
  line-height: 1.45;
  display: block;
  white-space: pre;
  tab-size: 4;
}
</style>
