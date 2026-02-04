import { federation } from '@module-federation/vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import type { InlineConfig, ViteDevServer } from 'vite'
import { build, createServer } from 'vite'

async function createViteServer(inlineConfig: InlineConfig): Promise<ViteDevServer> {
  const error = console.error
  console.error = (...args: any[]) => {
    if (
      typeof args[0] === 'string'
      && args[0].includes('WebSocket server error:')
    ) {
      return
    }
    error(...args)
  }

  const server = await createServer(inlineConfig)

  console.error = error
  return server
}

export async function createBuildServer(options: { dev?: boolean }): Promise<void> {
  const config: InlineConfig = {
    plugins: [
      federation({
        // filename: 'remoteEntry.js',
        name: 'remote',
        manifest: true,
        exposes: {
          './index': './src/index.ts',
        },
        shared: ['vue', 'vue-router'],
      }),
      vue(),
      vueJsx(),
    ],
    resolve: {
      alias: {
        // '@': path.resolve(__dirname, 'src'),
      },
    },
  }

  if (options.dev) {
    const viteServer = await createViteServer(config)

    await viteServer.listen()

    viteServer.printUrls()
    viteServer.bindCLIShortcuts({ print: true })
  }
  else {
    await build(config)
  }
}
