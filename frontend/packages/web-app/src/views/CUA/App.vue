<script lang="ts" setup>
import { BorderMotion } from '@rpa/components'
import { useToggle } from '@vueuse/core'
import { onMounted, onUnmounted, ref } from 'vue'

import ConfigProvider from '@/components/ConfigProvider/index.vue'

import Header from './Header.vue'
import ChainOfThought from './ChainOfThought.vue'
import type { PartialToolCall, Step } from './utils'
import { createStep, processStreamResponse } from './utils'

const [isExpanded, toggleExpanded] = useToggle(false)

const steps = ref<Step[]>([])
const isStreaming = ref(false)
let abortController: AbortController | null = null

function markAllComplete() {
  steps.value.forEach((s) => {
    if (s.status !== 'complete')
      s.status = 'complete'
  })
}

async function startRequest(userMessage: string) {
  if (isStreaming.value)
    return
  isStreaming.value = true
  steps.value = []

  abortController = new AbortController()

  const partialToolCalls: Record<number, PartialToolCall> = {}
  let currentTextStepId: string | null = null

  try {
    const response = await fetch(
      'http://localhost:13159/api/rpa-ai-service/cua/chat/stream',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'user', content: [{ type: 'text', text: userMessage }] }],
        }),
        signal: abortController.signal,
      },
    )

    if (!response.ok || !response.body) {
      const errorStep = createStep('text', `请求失败: ${response.status} ${response.statusText}`)
      errorStep.status = 'complete'
      steps.value.push(errorStep)
      return
    }

    await processStreamResponse(
      response.body.getReader(),
      { steps: steps.value, partialToolCalls, currentTextStepId },
      {
        onUpdateCurrentTextStepId: id => (currentTextStepId = id),
        onMarkAllComplete: markAllComplete,
      },
    )

    markAllComplete()
  }
  catch (err: any) {
    if (err?.name !== 'AbortError') {
      const errorStep = createStep('text', `流式响应出错: ${err?.message ?? String(err)}`)
      errorStep.status = 'complete'
      steps.value.push(errorStep)
    }
  }
  finally {
    isStreaming.value = false
  }
}

function handlePause() {
  if (abortController) {
    abortController.abort()
    isStreaming.value = false
    markAllComplete()
  }
}

onMounted(() => {
  startRequest('帮我点击搜索按钮')
})

onUnmounted(() => {
  abortController?.abort()
})
</script>

<template>
  <ConfigProvider>
    <div class="cua-container">
      <div class="motion-layer">
        <BorderMotion />
      </div>

      <div class="panel-layer" :class="isExpanded ? 'items-center justify-center' : 'items-end justify-end p-6'">
        <div
          class="cua-content-container border-border border-[1px] bg-white"
          :class="isExpanded ? 'w-[840px] h-[640px] rounded-3xl p-6' : 'w-[275px] rounded-2xl p-3 gap-2'"
        >
          <Header
            :is-streaming="isStreaming"
            :is-expanded="isExpanded"
            @toggleExpanded="toggleExpanded"
            @pause="handlePause"
          />
          <ChainOfThought
            v-if="isExpanded"
            :steps="steps"
            :is-streaming="isStreaming"
            class="mt-6"
          />
        </div>
      </div>
    </div>
  </ConfigProvider>
</template>

<style scoped>
.cua-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.motion-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.panel-layer {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  pointer-events: none;
  z-index: 1;
}

.panel-layer > * {
  pointer-events: auto;
}

.cua-content-container {
  box-shadow: 0 12px 16px -4px rgba(10, 13, 18, 0.08), 0 4px 6px -2px rgba(10, 13, 18, 0.03);
}
</style>
