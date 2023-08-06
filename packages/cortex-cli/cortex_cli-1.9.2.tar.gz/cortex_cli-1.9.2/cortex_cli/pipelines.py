from   plumbum      import cli
from   cortex_cli.cli_api_base import CliApiBase
import requests

class PipelinesCli(cli.Application):
    NAME = 'pipelines'

class PipelinesBase(CliApiBase):
    _id = cli.SwitchAttr(
        names     = ['-i','--id'], 
        argtype   = str,
        mandatory = True
    )

    def main(self, *args):
        args_list = self._check_args_not_empty(args)
        action    = args_list[0]

        response = self._get_pipeline()
        response = self._deploy(action, response['modelId'])
    

    def _get_pipeline(self) -> dict:
        return self._handle_api_response(requests.get(
            url     = f'{self.endpoint}/{self._id}',
            headers = self.headers
        ))['documents']

    def _deploy(self, action: str):
        response = requests.put(
            url     = f'{self.endpoint}/{self._id}/{action}',
            headers = self.headers,
            json    = {'modelId': self._model_id}            
        )
        
        return self._handle_api_response(response, f'Deploying the Model from pipeline {self._id}')


@PipelinesCli.subcommand('deploy')
class PipelinesDeploy(PipelinesBase):
    def main(self, *args):
        return super().main('deploy')

@PipelinesCli.subcommand('undeploy')
class PipelinesUndeploy(PipelinesBase):
    def main(self, *args):
        return super().main('undeploy')
