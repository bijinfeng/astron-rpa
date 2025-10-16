import { defineConfig } from 'tsdown'

import packageJson from './package.json'

export default defineConfig({
  entry: 'src/index.ts',
  format: 'esm',
  dts: {
    sourcemap: true,
  },
  define: {
    RPA_VERSION: packageJson.version,
  },
})
