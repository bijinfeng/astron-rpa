<script lang="ts" setup>
import ChainOfThought from './ChainOfThought.vue'

const emit = defineEmits(['close'])

function handleClose() {
  emit('close')
}
</script>

<template>
  <div class="cua-expanded-container w-[840px] h-[640px] bg-white rounded-3xl p-6 border-border">
    <div class="flex items-center h-8 mb-6">
      <div class="text-base font-semibold truncate flex-1">
        Agent操作中
      </div>

      <div class="w-8 h-8 flex items-center justify-center">
        <rpa-hint-icon name="close-1" class="text-base" enable-hover-bg @click="handleClose" />
      </div>
    </div>

    <div class="rounded-xl p-4 border-border border-[1px]">
      <ChainOfThought />
    </div>
  </div>
</template>

<style scoped>
.cua-expanded-container {
  box-shadow: 0 12px 16px -4px rgba(10, 13, 18, 0.08), 0 4px 6px -2px rgba(10, 13, 18, 0.03);
}
</style>