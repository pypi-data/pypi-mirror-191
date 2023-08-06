from cookiecutter.main import cookiecutter
from plumbum import cli, local
import requests
from collections import namedtuple
import cortex_cli.api.github_api as gh

import traceback
import os
import os.path
import mlflow
import yaml
import sys
import importlib
from datetime import datetime
from mlflow.models.signature import infer_signature
from os import walk

from cortex_cli.cli_api_base import CliApiBase

from cortex_core._ethics_checks import EthicsResult
from cortex_core._drift_checks import DriftResult


class ModelsCli(cli.Application):
    NAME = 'models'


@ModelsCli.subcommand('init')
class InitModel(CliApiBase):
    _model_name = cli.SwitchAttr(
        names=['-n', '--name'],
        argtype=str,
        help='The name of the repository. Should use dash case, ie. digits-model',
        mandatory=True
    )

    _description = cli.SwitchAttr(
        names=['-d', '--description'],
        argtype=str,
        default='A model that is initialized through the Cortex CLI.',
        help='A description of the model'
    )

    _token = cli.SwitchAttr(
        names=['--github-token'],
        argtype=str,
        envname='GH_TOKEN',
        mandatory=True
    )

    _org = cli.SwitchAttr(
        names=['--github-org'],
        argtype=str,
        envname='GH_ORG',
        default='nearlyhuman',
    )

    _path = cli.SwitchAttr(
        names=['-p', '--path'],
        argtype=str,
        envname='MODEL_PATH',
        default='.',
    )

    _register = cli.Flag(
        names=["-r", "--register"]
    )

    # Cookie Cutter Model Template
    _github_ml_template = cli.SwitchAttr(
        names=['-m', '--model-template'],
        argtype=str,
        default='ml-model-template',
        help='The template repository for creating a new client specific ML Pipeline project'
    )

    def main(self, *args):
        github = gh.Github(
            self._model_name,
            self._github_ml_template,
            self._description,
            # TODO: Need to separate out this organization because the GH account can be from anywhere.
            self._org,
            self._token
        )

        template_repo = 'git+ssh://git@github.com/{}/{}.git'.format(
            github.owner,
            github.template_name
        )

        self._validate_repo(github)
        self._generate_template_repo(template_repo, github)
        self._create_repo(template_repo, github)
        self._register_model()

    def _validate_repo(self, github_api: gh.Github):
        path = f'../{self._model_name}'

        if os.path.exists(path):
            error = f'The directory "{self._org}/{self._model_name}" already exists. Either rename the directory or register the repository directly.'

        if (self._get_github_repo(github_api)):
            error = f'Found existing GitHub repository "{self._org}/{self._model_name}" - please use a different name.'

        if error:
            raise Exception(error)

    def _generate_template_repo(self, template_repo, github):
        cookiecutter(
            template_repo,
            no_input=True,
            output_dir='..',
            extra_context={
                'model_name':  self._model_name.replace('-', ' ').title(),
                'description': github.description
            }
        )

    def _create_repo(self, template_repo, github):
        # What is going on here? Messing with directories like this seems suspect
        cd = local['cd']
        cd('../{}'.format(github.repo_name))

        # create the repository in github
        response = self._handle_api_response(gh.create_repo(github))

        # commit and push to the new repo in github
        repo = gh.Repo(path=self._path)
        repo.init() \
            .set_remote(github.owner, github.repo_name) \
            .add() \
            .commit('Initial commit. Generated from Cortex CLI using the model template {}.'.format(template_repo)) \
            .push()

        self._pass(
            f'Created the GitHub repository "{self._org}/{self._model_name}"')
        return response

    def _register_model(self, model_name: str):
        if self._register:
            response = requests.post(
                url=self.endpoint,
                headers=self.headers,
                json={
                    'name': model_name,
                    'repo': model_name
                }
            )
            self._handle_api_response(
                response, f'Registered the model repository {response["_id"]}')
        else:
            self._fail(
                'Skipping Cortex registration. Please register the repository with Cortex before training in the cloud')


@ModelsCli.subcommand('register')
class RegisterModel(CliApiBase):
    _repo = cli.SwitchAttr(
        names=['-r', '--repo'],
        argtype=str,
        mandatory=True
    )

    def main(self, *args):
        response = self._register_model()
        self._print(response)

    def _register_model(self):
        return self._handle_api_response(requests.post(
            url=self.endpoint,
            headers=self.headers,
            json={
                'name': self._repo,
                'repo': self._repo
            }
        ))


@ModelsCli.subcommand('run')
class RunModelPipeline(CliApiBase):
    _path = cli.SwitchAttr(
        names=['-p', '--path'],
        argtype=str,
        envname='MODEL_PATH',
        default='.',
    )

    _tracking = cli.Flag(
        names=['-t', '--tracking']
    )

    # Properties

    @property
    def _model_id(self):
        return self._model_json['_id'] if self._model_json else None

    @property
    def _pipeline_id(self):
        return self._pipeline_json['_id'] if self._pipeline_json else None

    modules = {}
    @property
    def _modules(self):
        if self.modules:
            return self.modules
        for (root, dir_names, file_names) in walk(self._config['module_path']):
            file_names[:] = [
                f for f in file_names 
                if f.endswith('.py') and f not in ['__init__.py', '{}.py'.format(self._config['model_module'])] 
            ]
            # TODO: Set map of file path locations to module name
            for f in file_names:
                self.modules['{}/{}'.format(root, f)] = f.replace('.py', '')
        return self.modules

    @property
    def _model_module(self):
        return '{}/{}.py'.format(self._config['module_path'], self._config['model_module'])
    
    @property
    def _model_dir(self):
        return self._config['module_path']
    
    @property
    def _artifacts_dir(self):
        location = 'cortex' if self._tracking else 'local'
        id = self._pipeline_id if self._tracking and self._pipeline_id else self._now
        return f'models/{location}/{id}'
    
    @property
    def _pipeline_steps(self):
        Step = namedtuple('Step', 'name type')
        return [Step(dict[list(dict.keys())[0]], list(dict.keys())[0]) for dict in self._config['pipeline_steps']]

    _now = datetime.now().strftime('%m%d%Y-%H%M%S')

    @property
    def _config(self):
        return self._read_yaml('cortex.yml')

    # Helpers

    def _load_module(self, module_path, module_name):
        print('\t\tLoading module {} from {}'.format(module_name, module_path))
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def _read_yaml(self, file: str) -> dict:
        if not os.path.exists(file):
            self._fail(f'Error! No "{file}" found in this Model project.')

        with open(file, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

# -------------------------------------------------------------------------------

    def main(self, *args):
        # Change to working directory
        os.chdir(self._path)

        model = None
        self._error_message = None
        self._success = False
        try:
            self._model_json = self._get_model()
            # Step 1 - Get live model data
            if self._tracking:
                self._mlflow_client = self._setup_mlflow()
                self._setup_pipeline()

            # Step 2 - Load the Model Class
            model = self._instantiate_model(self._config)

            # Step 3 - Initialize the pipeline steps
            self._initialize_steps()

            # Step 4 - Run the pipeline
            if self._tracking:
                self._pipeline_json = self._run_pipeline()

            # Step 5 - Run the pipeline steps
            self._run_pipeline_steps(model)

            # Step 6 - Save the pipeline artifacts
            self._save_pipeline(model)

            # Step 7 - Upload the pipeline artifacts
            if self._tracking:
                self._upload_pipeline()
        except Exception as e:
            pass
            # self._error_message = traceback.format_exc()#str(e)
        finally:
            # Step 8 - Contact callback route to update currentStage of model pipeline
            if self._tracking and self._pipeline_json and self._model_json:
                status = 'Failed' if self._error_message or not self._success else 'Successful'
                self._complete_callback(
                    status,
                    self._error_message
                )

            if self._error_message:
                self._fail(self._error_message)
            
            self._pass('Completed Cortex Pipeline Run')

# -------------------------------------------------------------------------------

    def _initialize_steps(self):
        # Convert yaml steps to ml-api format
        _steps = []
        for step in self._pipeline_steps:
            _steps.append({
                'name':   step.name,
                'type':   step.type,
                'config': {}
            })
        
        if self._tracking:
            # Set cortex steps
            self._steps = self._create_steps(_steps)
        else:
            # Set normal steps
            self._steps = _steps

        self._pass('Loaded pipeline steps')

    def _create_steps(self, _steps):
        response = requests.post(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/steps',
            headers=self._headers,
            json={
                'stepsConfig': _steps
            }
        ).json()

        if len(response) == 0:
            raise Exception('Error! Failed to load the pipeline steps.')
        
        return response

    def _complete_step(self, step, step_status, step_result, step_risk):
        json_value = None

        # Setup json value depending on if we have risk or not
        json_value = {
            'pipelineId':    step['pipelineId'],
            'name':          step['name'],
            'type':          step['type'],
            'order':         step['order'],
            'status':        step_status,
            'statusMessage': '' if step_result is None else str(step_result)
        }

        if step_risk != '':
            json_value['risk'] = step_risk

        return requests.put(
            url=f'{self._api_url}/steps/{step["_id"]}/complete',
            headers=self._headers,
            json=json_value
        ).json()

    def _get_drift_inferences(self):
        response = requests.get(
            url=f'{self._api_url}/inferences?modelId={self._model_id}&hasTags[]=Drift Detection',
            headers=self._headers
        ).json()

        inferences = []
        if response and len(response['documents']) > 0:
            for inference in response['documents']:
                if inference['successful']:
                    inferences.append((inference['_id'], [inference['inputs']['ndarray']], [inference['outputs']['ndarray']]))

        return inferences

# -------------------------------------------------------------------------------

    def _get_pipeline(self, git_branch, model_id):
        query = {
            'gitBranch': git_branch,
            'local':     False
        }

        response = requests.get(
            url=f'{self._api_url}/pipelines',
            params=query,
            headers=self._headers,
            json={'modelId': model_id}
        )

        # This is definitely wrong and it's weird how we check here
        # We should probably just catch a 404 and handle it?
        pipeline = response.json()['documents']
        if len(pipeline) == 1:
            message = f'Found existing pipeline {pipeline["_id"]} for branch {git_branch} with status {pipeline["currentStage"]}.'

            if pipeline['currentStage'] == 'Running':
                raise Exception(
                    f'{message} The cloud initiated training needs to complete first on this branch before running again.')

            if pipeline['currentStage'] == 'Pending':
                self._pass(message)
                return pipeline

        self._pass(f'Did not find existing pipeline for branch {git_branch}')
        return None

    def _create_pipeline(self, model_id, git_branch, git_hash):
        response = requests.post(
            url=f'{self._api_url}/pipelines',
            headers=self._headers,
            json={
                'modelId':   model_id,
                'gitBranch': git_branch,
                'gitHash':   git_hash,
                'local':     True
            }
        ).json()
        
        return response

    def _run_pipeline(self):
        return requests.put(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/run',
            headers=self._headers,
            json={
                'modelId': self._model_id
            }
        ).json()

    def _run_pipeline_steps(self, model):
        current_step = None
        try:
            for step in self._steps:
                current_step = step['type']
                step_func = getattr(model, current_step)
                step_result = None

                # Handle special case for passing testing inferences to test_predict function
                if current_step == 'detect_drift':
                    if self._tracking:
                        step_result = step_func(self._get_drift_inferences())
                    else:
                        step_result = 'Skipping drift detection. Requires tracking to be enabled.'
                else:
                    step_result = step_func()

                if self._tracking:
                    step_risk = ''

                    # Get ethics check results (if it exists)
                    if type(step_result) is EthicsResult:
                        # Parse out risk level
                        step_risk = step_result.risk.value

                        # Parse out result
                        step_result = step_result.result_str
                    elif type(step_result) is DriftResult:
                        # Parse out result
                        step_result = step_result.result_str

                    self._complete_step(step, 'Successful',
                                        step_result, step_risk)
                self._pass(
                    f'{step["name"]} completed successfully')
            self._success = True
        except Exception as e:
            if self._tracking:
                self._complete_step(step, 'Failed', str(e), '')
            self._error_message = f'{step["name"]} completed with an error.\n{traceback.format_exc()}'

    def _setup_pipeline(self):
        # Get the local branch
        git_branch = gh.Repo().branch
        git_hash = gh.Repo().hash

        # Look for an existing 'Pending' pipeline for this branch
        pipeline_response = self._get_pipeline(
            git_branch,
            self._model_id
        )

        if pipeline_response:
            self._pipeline_json = self._handle_api_response(pipeline_response)
            return

        # If not found, create the locally sourced pipeline
        self._pipeline_json = self._create_pipeline(
            self._model_id,
            git_branch,
            git_hash
        )

        self._pass(f'Pipeline {self._pipeline_json["currentStage"]} with id: {self._pipeline_id}')

# -------------------------------------------------------------------------------

    def _get_model(self):
        query = {
            'repo': gh.Repo().repo
        }

        response = requests.get(
            url=self._endpoint,
            params=query,
            headers=self._headers
        )

        model = response.json()['documents']

        if response.status_code != 200 or len(model) != 1:
            raise Exception('Error! This model could not be found')

        self._pass(
            f'Found the model {gh.Repo().repo}')

        return model[0]

    def _complete_callback(self, status, error_message=None):
        body = {
            'modelId':      self._model_id,
            'currentStage': status,
        }

        if error_message:
            body['message']: error_message

        requests.put(
            url=f'{self._api_url}/pipelines/{self._pipeline_id}/run/complete',
            headers=self._headers,
            json=body
        )

    def _save_pipeline(self, model):
        # TODO: How to generalize this infer signature call
        signature = infer_signature(model.input_example, model.output_example)

        # Save model
        modules = list(self._modules.keys())
        modules.append(self._model_module)
        mlflow.pyfunc.save_model(
            python_model=model, 
            path=self._artifacts_dir,                   # Where artifacts are stored locally
            code_path=list(modules),                    # Local code paths not on
            conda_env='conda.yml',
            artifacts={},
            signature=signature
        )

        self._pass(f'Saved the pipeline artifacts to disk: ({self._artifacts_dir})')

    def _upload_pipeline(self):
        file_names = []
        file_paths = []

        # Get files from pipeline run
        for root, dirs, files in os.walk(self._artifacts_dir):
            for file in files:
                file_names.append(file)
                file_paths.append(os.path.join(root, file))

        body = {
            'fileNames': file_names
        }
        
        # Obtain individual file upload urls
        upload_urls = requests.post(
            f'{self._api_url}/pipelines/{self._pipeline_id}/files/upload',
            headers=self._headers,
            json=body
        ).json()

        # Upload each file individually
        for i in range(len(file_names)):
            with open(file_paths[i], 'rb') as f:
                requests.put(
                    upload_urls[i],
                    data=f.read()
                )
        
        self._pass(f'Uploaded the pipeline artifacts to Cortex')

    def _instantiate_model(self, config):
        # LOAD DEPENDENCY MODULES (except model)
        for path, module in self._modules.items():
            self._load_module(path, module)

        # LOAD MODEL MODULE
        model_module = self._load_module(
            '{}/{}.py'.format(config['module_path'], config['model_module']),
            config['model_module']
        )

        # return getattr(model_module, config['model_class'])(config['params'], 'demo', gh.Repo())
        return getattr(model_module, config['model_class'])(config['params'], self._model_id, self._api_url, self._headers)

    def _setup_mlflow(self):
        # Create a client to make API calls to the tracking server
        return mlflow.tracking.MlflowClient()
