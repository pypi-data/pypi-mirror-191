# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zennews',
 'zennews.alerter',
 'zennews.cli',
 'zennews.materializers',
 'zennews.models',
 'zennews.pipelines',
 'zennews.steps',
 'zennews.steps.report',
 'zennews.steps.sources',
 'zennews.steps.summarize']

package_data = \
{'': ['*']}

install_requires = \
['bbc-feeds==2.1',
 'discord.py==2.1.0',
 'mdutils==1.4.0',
 'torch==1.13.1',
 'transformers==4.26.0',
 'zenml[server]==0.32.1']

entry_points = \
{'console_scripts': ['zennews = zennews.cli.base:cli']}

setup_kwargs = {
    'name': 'zennews',
    'version': '0.1.0',
    'description': 'ZenNews: Get summarized news on a schedule.',
    'long_description': '# ZenNews: Generate summarized news on a schedule\n\nProject description\n\n# The goal of the project\n\nPoints we would like to highlight: \n\n- The ease of use. It has a nice python SDK which would help you build apps\naround.\n- The same python SDK is extendable you can implement your own logic. There\nare two examples of that in this project.\n- There is a complete separation between the code and the infra. With one flag \nwe can switch between a local test setup to a remote deployment.\n- This is a small example that can easily be scaled up.\n\n# Structure of the implementation\n\n## PyPI package\n\nPyPI package explanation\n\nWhat is included in the package\n\n## Contents\n\n- pipeline\n- steps\n- custom materializer\n- custom stack component alerter\n- CLI application\n\n# Walkthrough\n\n## Test case\n\nlocal execution\n\n## Remote setting: GCP\n\nRemote GCP zenml server\n\n### Requirements\n\n- Service account\n- GCS artifact store\n- Vertex Orchestrator\n- GCP Secrets Manager\n- GCP Container Registry\n- Alerter (Optional)\n\n### Limitations\n\n- Vertex - Schedule\n- Schedule cancelling\n- Alerter (base interface)\n\n# How to contribute?\n\n# Future improvements and upcoming changes\n\n',
    'author': 'ZenML GmbH',
    'author_email': 'info@zenml.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zenml.io/project/zen-news-summarization',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
