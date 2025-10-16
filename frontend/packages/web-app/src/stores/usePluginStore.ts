import { computedAsync } from '@vueuse/core'
import { defineStore } from 'pinia'

import { getExtensions, initializePluginManager, loadPlugins } from '@/plugins/module-federation'

export const usePluginStore = defineStore('plugin', () => {
  const extensions = computedAsync(async () => {
    await initializePluginManager()
    await loadPlugins()

    return getExtensions()
  }, null)

  return { extensions }
})
