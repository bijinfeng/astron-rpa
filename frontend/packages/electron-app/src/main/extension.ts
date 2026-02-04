import fs from 'node:fs'
import path from 'node:path'
import type { IPluginConfig } from '@rpa/shared'

import { extensionPath, extensionBaseUrl } from './path'

interface MainManifest {
  name: string
  version: string
  description: string
  main: string
}

interface IExtension {
  name: string
  resourcePath: string
  config: IPluginConfig
}

export let extensions: IExtension[] = []

/**
 * 遍历 extensionPath 下的 package，读取 package.json 中的内容
 */
export function init() {
  const validExtensions: IExtension[] = []

  extensionPath.forEach((basePath) => {
    // 检查基础路径是否存在且为目录
    if (!fs.existsSync(basePath) || !fs.statSync(basePath).isDirectory()) {
      return
    }

    try {
      const items = fs.readdirSync(basePath)

      items.forEach((item) => {
        const itemPath = path.join(basePath, item)

        // 检查是否为目录
        if (fs.statSync(itemPath).isDirectory()) {
          const packageJsonPath = path.join(itemPath, 'package.json')

          // 检查 package.json 是否存在
          if (fs.existsSync(packageJsonPath) && fs.statSync(packageJsonPath).isFile()) {
            try {
              const content = fs.readFileSync(packageJsonPath, 'utf-8')
              const manifest: MainManifest = JSON.parse(content)
              const resourcePath = path.join(itemPath, 'dist')
              const entryUrl = `${extensionBaseUrl}${manifest.name}/remoteEntry.js`

              validExtensions.push({
                name: manifest.name,
                resourcePath,
                config: {
                  name: manifest.name,
                  version: manifest.version,
                  description: manifest.description,
                  entry: entryUrl,
                  enabled: true,
                }
              })
            } catch (err) {
              console.error(`Error parsing package.json in ${itemPath}:`, err)
            }
          } else {
            // 这里可以处理“空的包”或者没有 package.json 的包
            // 按照用户需求，目前主要是读取存在的 package.json
          }
        }
      })
    } catch (err) {
      console.error(`Error reading extension directory ${basePath}:`, err)
    }
  })

  extensions = validExtensions
}

init()

export const loadExtensions = () => extensions.map(it => it.config)

export const getExtensionResourcePath = (name: string) => {
  const extension = extensions.find(it => it.name === name)
  return extension?.resourcePath || ''
}
