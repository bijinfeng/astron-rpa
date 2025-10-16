import cac from 'cac'
import type { CAC } from 'cac'

function applyCommonOptions(cli: CAC) {
  cli
    .option(
      '-c, --config <config>',
      'specify the configuration file, can be a relative or absolute path',
    )
}

export function runCli(): void {
  const cli = cac('rpa')

  cli.help()
  cli.version(RPA_VERSION)

  applyCommonOptions(cli)
}
