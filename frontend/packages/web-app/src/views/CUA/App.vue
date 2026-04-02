<script lang="ts" setup>
import { BorderMotion } from '@rpa/components'
import { useToggle } from '@vueuse/core'

import ConfigProvider from '@/components/ConfigProvider/index.vue'

import CollapsedPanel from './CollapsedPanel.vue'
import ExpandedPanel from './ExpandedPanel.vue'

const [isExpanded, toggleExpanded] = useToggle(false)
</script>

<template>
  <ConfigProvider>
    <div class="cua-container">
      <!-- 背景动效层 - 点击穿透 -->
      <div class="motion-layer">
        <BorderMotion />
      </div>

      <!-- 交互层 - 可点击 -->
      <div class="panel-layer" :class="isExpanded ? 'items-center justify-center' : 'items-end justify-end p-6'">
        <ExpandedPanel v-if="isExpanded" @close="toggleExpanded(false)" />
        <CollapsedPanel v-else @expand="toggleExpanded(true)" />
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
</style>
