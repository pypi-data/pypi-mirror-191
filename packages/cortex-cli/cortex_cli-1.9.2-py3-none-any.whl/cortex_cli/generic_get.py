from cortex_cli.clients import ClientsCli
from plumbum import cli
from cortex_cli.cli_api_base import CliApiBase
from cortex_cli.inferences import InferencesCli
from cortex_cli.pipelines import PipelinesCli
import requests


@ClientsCli.subcommand('get')   # Weird, but technically valid
@InferencesCli.subcommand('get')
@PipelinesCli.subcommand('get')
class GetCli(CliApiBase):
    _id = cli.SwitchAttr(
        names=['-i', '--id'],
        argtype=str,
        help='The ID of the Cortex resource being queried.'
    )

    def main(self, *args):
        response = self._get()
        self._print(response)

    def _get(self):
        endpoint = f'{self._endpoint}/{self._id}' if self._id else self._endpoint
        response = self._handle_api_response(requests.get(
            url=endpoint, headers=self._headers), terminate=True)

        return response
