from plumbum.cli import Application
from cortex_cli.configure import ConfigureCli
from cortex_cli.clients import ClientsCli
from cortex_cli.inferences import InferencesCli
from cortex_cli.models import ModelsCli
from cortex_cli.pipelines import PipelinesCli

class CortexCli(Application):
    VERSION = '1.9.2'


def main():
    CortexCli.subcommand('configure', ConfigureCli)
    CortexCli.subcommand('clients', ClientsCli)
    CortexCli.subcommand('inferences', InferencesCli)
    CortexCli.subcommand('models', ModelsCli)
    CortexCli.subcommand('pipelines', PipelinesCli)

    CortexCli.run()


if __name__ == '__main__':
    main()
