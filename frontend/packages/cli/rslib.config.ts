import { defineConfig } from '@rslib/core'

export default defineConfig({
  lib: [
    {
      format: 'esm',
      syntax: 'es2021',
      dts: {
        bundle: false,
        distPath: './dist-types',
      },
      source: {
        entry: {
          index: './src/index.ts',
        },
        define: {
          RPA_VERSION: JSON.stringify(require('./package.json').version),
        },
      },
    },
  ],
})
