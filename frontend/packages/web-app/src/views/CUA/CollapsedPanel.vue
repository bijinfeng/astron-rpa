<script lang="ts" setup>
import { FlickerMotion } from '@rpa/components'

const emit = defineEmits(['expand'])

function handleExpand() {
  emit('expand')
}
</script>

<template>
  <div class="w-[275px] h-[56px] bg-white rounded-2xl p-3 flex items-center border-border gap-2">
    <FlickerMotion />

    <div class="text-base font-semibold truncate flex-1">
      Agent操作中
    </div>

    <div class="w-8 h-8 flex items-center justify-center">
      <rpa-hint-icon name="square" class="text-base" enable-hover-bg />
    </div>
    <a-divider type="vertical" class="h-4 m-0" />
    <div class="w-8 h-8 flex items-center justify-center">
      <rpa-hint-icon name="maximize" class="text-base" enable-hover-bg @click="handleExpand" />
    </div>
  </div>
</template>
