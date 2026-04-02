<script setup lang="ts">
import { useTranslation } from "i18next-vue";

import AtomFormItem from "./AtomFormItem.vue";

const { i18next } = useTranslation();

const props = defineProps<{
  atomFormMeta: RPA.Process.AtomTabs;
  nodeParameter: RPA.Process.NodeParameter;
}>()
</script>

<template>
  <article
    v-for="item in props.atomFormMeta.params"
    :key="item.key"
    class="tab-container text-[#333] dark:text-[rgba(255,255,255,0.45)]"
  >
    <div
      v-if="item.name"
      class="text-sm leading-6 mb-3 flex gap-1 items-center"
    >
      <span class="w-1 h-3 rounded-[1px] bg-primary" />
      {{ item.name[i18next.language] }}
    </div>
    <template v-for="it in item.formItems" :key="it.key">
      <AtomFormItem
        v-if="it.show !== false"
        :atom-form-item="it"
        @update="nodeParameter?.updateValue"
      />
    </template>
  </article>
</template>
