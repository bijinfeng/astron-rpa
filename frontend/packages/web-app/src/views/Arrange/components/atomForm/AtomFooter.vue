<script setup lang="ts">
import { baseUrl } from '@/utils/env'
import { WINDOW_NAME } from '@/constants'
import { windowManager, type CreateWindowOptions } from '@/platform'

import { useFormStore } from "./hooks/useFormStore";

const { atom } = useFormStore();

const handleRunDebug = async () => {
  const options: CreateWindowOptions = {
    url: `${baseUrl}/${WINDOW_NAME.CUA}.html`,
    title: WINDOW_NAME.CUA,
    label: WINDOW_NAME.CUA,
    alwaysOnTop: true,
    fullscreen: true,
    decorations: false,
    transparent: true,
  }

  await windowManager.createWindow(options, () => {
    windowManager.showWindow()
  })

  windowManager.hideWindow()
}
</script>

<template>
  <div class="flex" v-if="atom.debugButton">
    <a-button @click="handleRunDebug" v-if="atom.debugButton === 'ai_debug'">
      运行调试
    </a-button>
  </div>
</template>
