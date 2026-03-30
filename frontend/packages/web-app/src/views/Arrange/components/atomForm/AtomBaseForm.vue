<script setup lang="ts">
import { useTranslation } from "i18next-vue";
import { ref, computed, useTemplateRef, nextTick } from "vue";
import { useToggle } from "@vueuse/core";

import AtomFormItem from "./AtomFormItem.vue";
import { useProvideFormStore } from "./hooks/useFormStore";

const props = defineProps<{ collapsed?: boolean, headerClass?: string, bodyClass?: string }>();

const emit = defineEmits(["close", "toggleCollapsed"]);

const { i18next } = useTranslation();
const { atom, atomTab, formattedTabs, nodeParameter } = useProvideFormStore();

const activeKey = ref<number>(0);
const inputRef = useTemplateRef<HTMLInputElement>('inputRef')
const [isEdit, toggleEdit] = useToggle(false);

const atomName = computed(() => atom.value?.alias || atom.value?.title);

const handleAliasChange = (e: FocusEvent) => {
  const alias = (e.target as HTMLInputElement).value?.trim()
  if (alias && alias !== atomName.value) {
    nodeParameter.value.updateAlias(alias)
  }
  toggleEdit(false)
}

const handleAliasEdit = () => {
  toggleEdit(true)
  nextTick(() => inputRef.value?.focus())
}
</script>

<template>
  <div class="relative atom-config-container h-full flex flex-col">
    <div :class="props.headerClass">
      <div class="h-8 mb-2 flex gap-2 items-center">
        <div
          class="w-6 h-6 mr-1 rounded-lg bg-primary inline-flex items-center justify-center"
        >
          <rpa-icon :name="atom.icon" class="text-white text-base" />
        </div>

        <a-input
          v-if="isEdit"
          ref="inputRef"
          :default-value="atomName"
          class="max-w-[300px]"
          size="small"
          @press-enter="toggleEdit(false)"
          @blur="handleAliasChange"
        />
        <div v-else class="truncate text-base font-semibold">
          {{ atomName }}
        </div>
        <a-tooltip :title="atom.title" v-if="atom.alias">
          <rpa-icon name="info" class="text-base text-text-tertiary" />
        </a-tooltip>
        <rpa-icon
          name="edit-outlined"
          class="text-base cursor-pointer text-text-secondary"
          @click="!isEdit && handleAliasEdit()"
        />

        <div class="flex-1" />

        <rpa-hint-icon
          :name="props.collapsed ? 'maximize' : 'minimize'"
          :title="props.collapsed ? '切换到宽版' : '切换到窄版'"
          class="text-base mx-1"
          enable-hover-bg
          @click="() => emit('toggleCollapsed')"
        />

        <rpa-hint-icon
          name="close-1"
          class="text-base mx-1"
          enable-hover-bg
          @click="() => emit('close')"
        />
      </div>

      <div class="text-text-secondary mb-3 truncate">{{ atom.comment }}</div>

      <a-segmented
        v-model:value="activeKey"
        block
        :options="formattedTabs"
        class="mb-6"
      >
        <template #label="{ title }">
          <span class="text-[12px]">{{ $t(title) }}</span>
        </template>
      </a-segmented>
    </div>

    <div class="flex-1 overflow-y-auto" :class="props.bodyClass">
      <article
        v-for="item in atomTab[activeKey]?.params"
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
    </div>
  </div>
</template>

<style lang="scss" scoped>
.atom-config-container {
  opacity: 1;

  .tab-container {
    font-size: 12px;
    margin-bottom: 24px;
  }

  &::-webkit-scrollbar {
    width: 4px;
  }

  :deep(.ant-tabs-tab) {
    padding: 8px 16px;
  }

  :deep(.ant-tabs-tabpane) {
    padding: 0 10px 10px;
  }
}
</style>
