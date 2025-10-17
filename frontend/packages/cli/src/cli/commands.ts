import cac from 'cac'
import debug from 'debug'

import { version } from '../../package.json'
import { globalLogger } from '../logger'
import { resolveComma, toArray } from '../utils'

import { createBuildServer } from './vite'

const cli = cac('rpa')

cli.help().version(version)

cli.option('--debug [feat]', 'Show debug logs')

cli
  .command('dev', 'Start the development server')
  .action(async () => {
    await createBuildServer({ dev: true })
  })

cli
  .command('build', 'build the library for production')
  .option('-w, --watch', 'turn on watch mode, watch for changes and rebuild')
  .action(async () => {
    await createBuildServer({ dev: false })
  })

export async function runCli(): Promise<void> {
  cli.parse(process.argv, { run: false })

  if (cli.options.debug) {
    let namespace: string
    if (cli.options.debug === true) {
      namespace = 'rpa:*'
    }
    else {
      // support debugging multiple flags with comma-separated list
      namespace = resolveComma(toArray(cli.options.debug))
        .map(v => `rpa:${v}`)
        .join(',')
    }

    const enabled = debug.disable()
    if (enabled)
      namespace += `,${enabled}`

    debug.enable(namespace)
    debug('rpa:debug')('Debugging enabled', namespace)
  }

  try {
    await cli.runMatchedCommand()
  }
  catch (error) {
    globalLogger.error(error)
    process.exit(1)
  }
}
