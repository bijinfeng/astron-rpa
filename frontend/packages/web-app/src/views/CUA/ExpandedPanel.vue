<script lang="ts" setup>
const emit = defineEmits(['close'])

function handleClose() {
  emit('close')
}
</script>

<template>
  <div class="w-[840px] h-[640px] bg-white rounded-3xl p-6 border-border">
    <div class="flex items-center h-8 mb-6">
      <div class="text-base font-semibold truncate flex-1">
        Agent操作中
      </div>

      <div class="w-8 h-8 flex items-center justify-center">
        <rpa-hint-icon name="close-1" class="text-base" enable-hover-bg @click="handleClose" />
      </div>
    </div>

    <div class="rounded-xl px-4 border-border border-[1px]">
      xx
    </div>
  </div>
</template>
