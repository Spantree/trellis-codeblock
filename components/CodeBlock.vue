<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { createHighlighter } from 'shiki'
import type { Highlighter } from 'shiki'
import setiTheme from '../themes/seti.json'

interface Props {
  code: string
  language?: string
  theme?: string
  title?: string
  noChrome?: boolean
  fontSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  language: 'typescript',
  theme: 'Seti',
  noChrome: false,
  fontSize: 14,
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

onMounted(render)
watch(() => [props.code, props.language, props.theme], render)
</script>

<template>
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
      <div
        class="codeblock-code"
        :style="{ fontSize: fontSize + 'px' }"
        v-html="highlighted"
      />
    </div>
  </div>
</template>

<style scoped>
.codeblock-canvas {
  /* Carbon's light gray/cream gradient canvas */
  background: linear-gradient(135deg, #c0c5cc 0%, #b3bac2 100%);
  padding: 56px;
  border-radius: 4px;
  display: inline-block;
  max-width: 100%;
}

.codeblock-window {
  border-radius: 10px;
  overflow: hidden;
  /* Pronounced Carbon-style drop shadow */
  box-shadow: 0 20px 68px rgba(0, 0, 0, 0.55);
  background: #151718;
  min-width: 320px;
}

.codeblock-titlebar {
  position: relative;
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
  background: #151718;
  padding: 24px 32px;
  overflow-x: auto;
  overflow-y: hidden;
}

/* Reset Shiki's emitted <pre>/<code> to inherit our typography */
.codeblock-code :deep(pre.shiki) {
  margin: 0;
  padding: 0;
  background: transparent !important;
  overflow-x: auto;
}

.codeblock-code :deep(code) {
  font-family: 'Fira Code', 'Fira Mono', monospace;
  font-size: inherit;
  line-height: 1.45;
  display: block;
  white-space: pre;
  tab-size: 4;
}

/* Hide scrollbars while keeping scroll behavior */
.codeblock-code::-webkit-scrollbar,
.codeblock-code :deep(pre.shiki)::-webkit-scrollbar {
  height: 6px;
  background: transparent;
}

.codeblock-code::-webkit-scrollbar-thumb,
.codeblock-code :deep(pre.shiki)::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 3px;
}
</style>
