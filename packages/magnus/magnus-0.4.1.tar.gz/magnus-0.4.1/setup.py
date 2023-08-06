# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnus']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'click-plugins>=1.1.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'ruamel.yaml',
 'ruamel.yaml.clib',
 'stevedore>=3.5.0,<4.0.0',
 'yachalk']

extras_require = \
{'docker': ['docker'], 'notebook': ['ploomber-engine>=0.0.19,<0.0.20']}

entry_points = \
{'console_scripts': ['magnus = magnus.cli:cli'],
 'magnus.catalog.BaseCatalog': ['do-nothing = magnus.catalog:DoNothingCatalog',
                                'file-system = '
                                'magnus.catalog:FileSystemCatalog'],
 'magnus.datastore.BaseRunLogStore': ['buffered = '
                                      'magnus.datastore:BufferRunLogstore',
                                      'file-system = '
                                      'magnus.datastore:FileSystemRunLogstore'],
 'magnus.executor.BaseExecutor': ['demo-renderer = '
                                  'magnus.executor:DemoRenderer',
                                  'local = magnus.executor:LocalExecutor',
                                  'local-container = '
                                  'magnus.executor:LocalContainerExecutor'],
 'magnus.experiment_tracker.BaseExperimentTracker': ['do-nothing = '
                                                     'magnus.experiment_tracker:DoNothingTracker'],
 'magnus.integration.BaseIntegration': ['demo-renderer-run_log_store-buffered '
                                        '= '
                                        'magnus.integration:DemoRenderBufferedRunLogStore',
                                        'local-catalog-do-nothing = '
                                        'magnus.integration:LocalDoNothingCatalog',
                                        'local-container-catalog-do-nothing = '
                                        'magnus.integration:LocalContainerDoNothingCatalog',
                                        'local-container-catalog-file-system = '
                                        'magnus.integration:LocalContainerComputeFileSystemCatalog',
                                        'local-container-run_log_store-buffered '
                                        '= '
                                        'magnus.integration:LocalContainerComputeBufferedRunLogStore',
                                        'local-container-run_log_store-file-system '
                                        '= '
                                        'magnus.integration:LocalContainerComputeFileSystemRunLogstore',
                                        'local-container-secrets-dotenv = '
                                        'magnus.integration:LocalContainerComputeDotEnvSecrets',
                                        'local-container-secrets-environment = '
                                        'magnus.integration:LocalContainerComputeEnvSecretsManager',
                                        'local-run_log_store-buffered = '
                                        'magnus.integration:LocalComputeBufferedRunLogStore',
                                        'local-run_log_store-file-system = '
                                        'magnus.integration:LocalComputeFileSystemRunLogStore'],
 'magnus.nodes.BaseNode': ['as-is = magnus.nodes:AsISNode',
                           'dag = magnus.nodes:DagNode',
                           'fail = magnus.nodes:FailNode',
                           'map = magnus.nodes:MapNode',
                           'parallel = magnus.nodes:ParallelNode',
                           'success = magnus.nodes:SuccessNode',
                           'task = magnus.nodes:TaskNode'],
 'magnus.secrets.BaseSecrets': ['do-nothing = '
                                'magnus.secrets:DoNothingSecretManager',
                                'dotenv = magnus.secrets:DotEnvSecrets',
                                'env-secrets-manager = '
                                'magnus.secrets:EnvSecretsManager'],
 'magnus.tasks.BaseTaskType': ['notebook = magnus.tasks:NotebookTaskType',
                               'python = magnus.tasks:PythonTaskType',
                               'python-function = '
                               'magnus.tasks:PythonFunctionType',
                               'python-lambda = '
                               'magnus.tasks:PythonLambdaTaskType',
                               'shell = magnus.tasks:ShellTaskType']}

setup_kwargs = {
    'name': 'magnus',
    'version': '0.4.1',
    'description': 'A Compute agnostic pipelining software',
    'long_description': '# Hello from magnus\n\n\n![logo](docs/assets/logo1.png)\n---\n\n**Magnus** is a *thin* layer of abstraction over the underlying infrastructure to enable data scientist and\nmachine learning engineers. It provides:\n\n- A way to execute Jupyter notebooks/python functions in local or remote platforms.\n- A framework to define complex pipelines via YAML or Python SDK.\n- Robust and *automatic* logging to ensure maximum reproducibility of experiments.\n- A framework to interact with secret managers ranging from environment variables to other vendors.\n- Interactions with various experiment tracking tools.\n\n## What does **thin** mean?\n\n- We really have no say in what happens within your notebooks or python functions.\n- We do not dictate how the infrastructure should be configured as long as it satisfies some *basic* criteria.\n    - The underlying infrastructure should support container execution and an orchestration framework.\n    - Some way to handle secrets either via environment variables or secrets manager.\n    - A blob storage or some way to store your intermediate artifacts.\n    - A database or blob storage to store logs.\n- We have no opinion of how your structure your project.\n- We do not creep into your CI/CD practices but it is your responsibility to provide the same environment where ever\nthe execution happens. This is usually via git, virtual environment manager and docker.\n- We transpile to the orchestration framework that is used by your teams to do the heavy lifting.\n\n## What does it do?\n\n\n![works](docs/assets/work.png)\n\n### Shift Left\n\nMagnus provides patterns typically used in production environments even in the development phase.\n\n- Reduces the need for code refactoring during production phase of the project.\n- Enables best practices and understanding of infrastructure patterns.\n- Run the same code on your local machines or in production environments.\n\n:sparkles::sparkles:Happy Experimenting!!:sparkles::sparkles:\n\n\n## Documentation\n\n[More details about the project and how to use it available here](https://astrazeneca.github.io/magnus-core/).\n\n## Installation\n\n\nThe minimum python version that magnus supports is 3.8\n## pip\n\nmagnus is a python package and should be installed as any other.\n\n```shell\npip install magnus\n```\n\nWe recommend that you install magnus in a virtual environment specific to the project and also poetry for your\napplication development.\n\nThe command to install in a poetry managed virtual environment\n\n```\npoetry add magnus\n```\n\n## Example Run\n\nTo give you a flavour of how magnus works, lets create a simple pipeline.\n\nCopy the contents of this yaml into getting-started.yaml or alternatively in a python file if you are using the SDK.\n\n---\n!!! Note\n\n   The below execution would create a folder called \'data\' in the current working directory.\n   The command as given should work in linux/macOS but for windows, please change accordingly.\n\n---\n\n``` yaml\ndag:\n  description: Getting started\n  start_at: step parameters\n  steps:\n    step parameters:\n      type: task\n      command_type: python-lambda\n      command: "lambda x: {\'x\': int(x) + 1}"\n      next: step shell\n    step shell:\n      type: task\n      command_type: shell\n      command: mkdir data ; env >> data/data.txt # For Linux/macOS\n      next: success\n      catalog:\n        put:\n          - "*"\n    success:\n      type: success\n    fail:\n      type: fail\n```\n\nThe same could also be defined via a Python SDK.\n\n```python\n\n#in pipeline.py\nfrom magnus import Pipeline, Task\n\ndef pipeline():\n    first = Task(name=\'step parameters\', command="lambda x: {\'x\': int(x) + 1}", command_type=\'python-lambda\',\n                next_node=\'step shell\')\n    second = Task(name=\'step shell\', command=\'mkdir data ; env >> data/data.txt\',\n                  command_type=\'shell\', catalog={\'put\': \'*\'})\n\n    pipeline = Pipeline(name=\'getting_started\')\n    pipeline.construct([first, second])\n    pipeline.execute(parameters_file=\'parameters.yaml\')\n\nif __name__ == \'__main__\':\n    pipeline()\n\n```\n\nSince the pipeline expects a parameter ```x```, lets provide that using ```parameters.yaml```\n\n```yaml\nx: 3\n```\n\n\nAnd let\'s run the pipeline using:\n``` shell\n magnus execute --file getting-started.yaml --parameters-file parameters.yaml\n```\n\nIf you are using the python SDK:\n\n```\npoetry run python pipeline.py\n```\n\nYou should see a list of warnings but your terminal output should look something similar to this:\n\n``` json\n{\n    "run_id": "20230131195647",\n    "dag_hash": "",\n    "use_cached": false,\n    "tag": "",\n    "original_run_id": "",\n    "status": "SUCCESS",\n    "steps": {\n        "step parameters": {\n            "name": "step parameters",\n            "internal_name": "step parameters",\n            "status": "SUCCESS",\n            "step_type": "task",\n            "message": "",\n            "mock": false,\n            "code_identities": [\n                {\n                    "code_identifier": "e15d1374aac217f649972d11fe772e61b5a2478d",\n                    "code_identifier_type": "git",\n                    "code_identifier_dependable": true,\n                    "code_identifier_url": "INTENTIONALLY REMOVED",\n                    "code_identifier_message": ""\n                }\n            ],\n            "attempts": [\n                {\n                    "attempt_number": 0,\n                    "start_time": "2023-01-31 19:56:55.007931",\n                    "end_time": "2023-01-31 19:56:55.009273",\n                    "duration": "0:00:00.001342",\n                    "status": "SUCCESS",\n                    "message": ""\n                }\n            ],\n            "user_defined_metrics": {},\n            "branches": {},\n            "data_catalog": []\n        },\n        "step shell": {\n            "name": "step shell",\n            "internal_name": "step shell",\n            "status": "SUCCESS",\n            "step_type": "task",\n            "message": "",\n            "mock": false,\n            "code_identities": [\n                {\n                    "code_identifier": "e15d1374aac217f649972d11fe772e61b5a2478d",\n                    "code_identifier_type": "git",\n                    "code_identifier_dependable": true,\n                    "code_identifier_url": "INTENTIONALLY REMOVED",\n                    "code_identifier_message": ""\n                }\n            ],\n            "attempts": [\n                {\n                    "attempt_number": 0,\n                    "start_time": "2023-01-31 19:56:55.128697",\n                    "end_time": "2023-01-31 19:56:55.150878",\n                    "duration": "0:00:00.022181",\n                    "status": "SUCCESS",\n                    "message": ""\n                }\n            ],\n            "user_defined_metrics": {},\n            "branches": {},\n            "data_catalog": [\n                {\n                    "name": "data/data.txt",\n                    "data_hash": "7e91b0a9ff8841a3b5bf2c711f58bcc0cbb6a7f85b9bc92aa65e78cdda59a96e",\n                    "catalog_relative_path": "20230131195647/data/data.txt",\n                    "catalog_handler_location": ".catalog",\n                    "stage": "put"\n                }\n            ]\n        },\n        "success": {\n            "name": "success",\n            "internal_name": "success",\n            "status": "SUCCESS",\n            "step_type": "success",\n            "message": "",\n            "mock": false,\n            "code_identities": [\n                {\n                    "code_identifier": "e15d1374aac217f649972d11fe772e61b5a2478d",\n                    "code_identifier_type": "git",\n                    "code_identifier_dependable": true,\n                    "code_identifier_url": "INTENTIONALLY REMOVED",\n                    "code_identifier_message": ""\n                }\n            ],\n            "attempts": [\n                {\n                    "attempt_number": 0,\n                    "start_time": "2023-01-31 19:56:55.239877",\n                    "end_time": "2023-01-31 19:56:55.240116",\n                    "duration": "0:00:00.000239",\n                    "status": "SUCCESS",\n                    "message": ""\n                }\n            ],\n            "user_defined_metrics": {},\n            "branches": {},\n            "data_catalog": []\n        }\n    },\n    "parameters": {\n        "x": 4\n    },\n    "run_config": {\n        "executor": {\n            "type": "local",\n            "config": {\n                "enable_parallel": false,\n                "placeholders": {}\n            }\n        },\n        "run_log_store": {\n            "type": "buffered",\n            "config": {}\n        },\n        "catalog": {\n            "type": "file-system",\n            "config": {\n                "compute_data_folder": "data",\n                "catalog_location": ".catalog"\n            }\n        },\n        "secrets": {\n            "type": "do-nothing",\n            "config": {}\n        },\n        "experiment_tracker": {\n            "type": "do-nothing",\n            "config": {}\n        },\n        "variables": {},\n        "pipeline": {\n            "start_at": "step parameters",\n            "name": "getting_started",\n            "description": "",\n            "max_time": 86400,\n            "steps": {\n                "step parameters": {\n                    "mode_config": {},\n                    "next_node": "step shell",\n                    "command": "lambda x: {\'x\': int(x) + 1}",\n                    "command_type": "python-lambda",\n                    "command_config": {},\n                    "catalog": {},\n                    "retry": 1,\n                    "on_failure": "",\n                    "type": "task"\n                },\n                "step shell": {\n                    "mode_config": {},\n                    "next_node": "success",\n                    "command": "mkdir data ; env >> data/data.txt",\n                    "command_type": "shell",\n                    "command_config": {},\n                    "catalog": {\n                        "put": "*"\n                    },\n                    "retry": 1,\n                    "on_failure": "",\n                    "type": "task"\n                },\n                "success": {\n                    "mode_config": {},\n                    "type": "success"\n                },\n                "fail": {\n                    "mode_config": {},\n                    "type": "fail"\n                }\n            }\n        }\n    }\n}\n```\n\nYou should see that ```data``` folder being created with a file called ```data.txt``` in it.\nThis is according to the command in ```step shell```.\n\nYou should also see a folder ```.catalog``` being created with a single folder corresponding to the run_id of this run.\n\nTo understand more about the input and output, please head over to the\n[documentation](https://project-magnus.github.io/magnus-core/).\n',
    'author': 'Vijay Vammi',
    'author_email': 'vijay.vammi@astrazeneca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AstraZeneca/magnus-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
