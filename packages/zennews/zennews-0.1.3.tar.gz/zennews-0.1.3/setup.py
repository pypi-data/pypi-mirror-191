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
    'version': '0.1.3',
    'description': 'ZenNews: Get summarized news on a schedule.',
    'long_description': "# ZenNews: Generate summarized news on a schedule\n\nIn today's information age, we are bombarded with a constant stream of news \nand media from a variety of sources. Summarizing tasks, particularly when it \ncomes to news sources, can be a powerful tool for efficient consumption of \ninformation. They distill complex or lengthy content into easily \ndigestible chunks that can be scanned and absorbed quickly, allowing us to \nkeep up with the news without being overwhelmed. They can also help us separate \nthe signal from the noise, highlighting the most important details and helping \nus identify what's worth further investigation. \n\nThis is where **ZenNews** come into the play. It offers a tool which can \nautomate the summarization process and save users time and effort while \nproviding them with the information they need. This can be particularly valuable \nfor busy professionals or anyone who wants to keep up with the news but doesn't \nhave the time to read every article in full.\n\n# The goal of the project\n\nThe definition of the concrete use-case aside, this project aims to showcase \nsome of the advantages that ZenML brings to the table. Some major points we \nwould like to highlight include:\n\n- **The ease of use**: ZenML features a simple and clean Python SDK. As you can \nobserve in this example, it is not only used to define your steps and \npipelines but also to access/manage the resources and artifacts that you \ninteract with along the way. This makes it significantly easier for our users \nto build their applications around ZenML.\n\n- **The extensibility**: ZenML is an extendable framework. ML projects often \nrequire custom-tailored solutions and what you get out-of-the-box may not be \nwhat you need. This is why ZenML is using base abstractions to allow you \nto create your own solutions without reinventing the whole wheel. You can find \ngreat examples of this feature by taking a look at the custom materializer \n(ArticleMaterializer) and the custom stack component (DiscordAlerter) \nimplemented within the context of this project.\n\n- **Stack vs Code**: One of the main features of ZenML is rooted within the \nconcept of our stacks. As you follow this example, you will see that there is a \ncomplete separation between the code and the infrastructure that the pipeline \nis running on. In fact, by utilizing just one flag, it is possible to switch \nfrom a local default stack to a remote deployment with scheduled pipelines.\n\n- **The scalability**: This is a small PoC-like example which aims to prove \nthat ZenML can help you streamline your workflows and accelerate your \ndevelopment process. However, it barely scratches the surface of how you can \nimprove it even further. For more information, check this section.\n\n# Walkthrough\n\n## Base installation\n\nThe `ZenNews` project is designed as a [PyPI package](https://pypi.org/project/zennews/)\nthat you can install it through `pip`:\n\n```bash\npip install zennews\n```\n\nThe package comes equipped with the following set of key pieces:\n\n- **The pipeline**: The `zen_news_pipeline` is the main pipeline in this \nworkflow. In total, it features three separate steps, namely `collect`, \n`summarize` and `report`. The first step is responsible for collecting \ndata, the second step summarizes them and the last step creates a report and \nposts it.\n- **The steps**: There is a concrete implementation for each step defined above.\n  - For the `collect` step, we have the `bbc_news_source` which (on default) \n  collects the top stories off of the BBC news feed and prepares `Article` \n  objects. \n  - For the `summarize` step, we have implemented `bart_large_cnn_samsum`\n  step. As the name suggests, it uses bart model to generate summaries. \n  - Ultimately, for the `report` step, we have implemented the `post_summaries` \n  step. It showcases how a generalized step can function within a ZenML \n  pipeline and uses an alerter to share the results.\n- **The materializer**: As mentioned above, the steps within our pipeline are \nusing the concept of `Article`s to define their input and output space. Through\nthis, we can show how to handle the materialization of these artifacts when it \ncomes a data type that is not a built-in.\n- **The custom stack component**: The ultimate goal of an application such as \n`ZenNews` is to display to outcomes to the user directly. With this project, \nwe have used this as a chance to show the extensibility of ZenML in terms of the\nstack components and implemented a `DiscordAlerter`.\n- **The CLI application**: The example also includes a Click CLI application. \nIt utilizes how easily you can use our Python SDK to build your application \naround your ZenML workflows. In order to see it action simply execute:\n  ```bash\n  zennews --help \n  ```\n\n## Test it locally right away\n\nOnce you installed the `zennews` package, you are ready to test it out locally \nright away. The following command will get the top five articles from the BBC\nnews feed, summarize them and present the results to you. \n\n> Warning: This will temporarily switch your active ZenML stack to the \n> **default** stack and when the pipeline runs, you will download the model \n> to your local machine.\n\nIn order to execute it, simply do:\n\n```bash\nzennews bbc\n```\n\nYou can also parameterize this process. In order to see the possible \nparameters, please use:\n\n```bash\nzennews bbc --help\n```\n\n## Switching to scheduled pipelines with Vertex\n\nThe potential of an application like `ZenNews` can be only unlocked by scheduling \nsummarization pipelines instead of manually triggering them. In order to showcase it, we \nwill set up a fully remote GCP stack and use the `VertexOrchestrator` to \nschedule the pipeline.\n\n### Deploy ZenML on GCP\n\nBefore you start building the stack, you need to deploy ZenML. For more \ninformation on how you can achieve do that on GCP, please check \n[the corresponding docs page](https://docs.zenml.io/getting-started/deploying-zenml).\n\n### ZenNews Stack\n\nOnce the ZenML is deployed, we can start to build up our stack. Our stack will \nconsist of the following components:\n\n- [GCP Secrets Manager](https://docs.zenml.io/component-gallery/secrets-managers/gcp)\n- [GCP Container Registry](https://docs.zenml.io/component-gallery/container-registries/gcloud)\n- [GCS Artifact Store](https://docs.zenml.io/component-gallery/artifact-stores/gcloud-gcs)\n- [Vertex Orchestrator](https://docs.zenml.io/component-gallery/orchestrators/gcloud-vertexai)\n- [Discord Alerter (part of the zennews package)](src/zennews/alerter/discord_alerter.py)\n \nThe first step is to install the `gcp` integration:\n\n```bash\nzenml integration install gcp\n```\n\n#### Secrets Manager\n\n```bash\nzenml secrets-manager register <NAME> \\\n    --flavor=gcp \\\n    --project_id=<PROJECT_ID>\n```\n\n#### Container Registry\n\n```bash\nzenml container-registry register <NAME> \\\n    --flavor=gcp \\\n    --uri=<REGISTRY_URI>\n```\n\n#### Artifact Store\n\n```bash\nzenml secrets-manager secret register <SECRET_NAME> \\\n    -s gcp \\\n    --token=@path/to/token/file.json\n```\n\n```bash \nzenml artifact-store register <NAME> \\\n    --flavor=gcp \\\n    --path=<PATH_TO_BUCKET> \\\n    --authentication_secret=<SECRET_NAME>\n```\n\n#### Orchestrator\n\n```bash\nzenml orchestrator register <NAME> \\\n    --flavor=vertex \\\n    --project=<PROJECT_ID> \\\n    --location=<GCP_LOCATION>\n```\n\n#### Alerter \n\n```bash\nzenml secrets-manager secret register <SECRET_NAME> \\\n    --web_hook_url=<WEBHOOK_URL>\n```\n```bash\nzenml alerter flavor register zennews.alerter.discord_alerter_flavor.DiscordAlerterFlavor\n```\n\n```bash \nzenml alerter flavor list\n```\n\n```bash\nzenml alerter register <NAME> \\\n    --flavor discord-webhook \\\n    --webhook_url_secret=<SECRET_NAME>\n```\n\n### Using the `zennews` CLI\n\nNow the stack is set up, you can use the `--schedule` option when you run your \n`zennews` pipeline. There are three possible values that you can use for the \n`schedule` option: `hourly`, `daily` (every day at 9 AM) or `weekly` (every\nMonday at 9 AM).\n\n```bash\nzennews bbc --schedule daily\n```\n\n## Limitations\n\n- One source\n- Schedule cancelling\n- Vertex - Schedule\n- Alerter (base interface)\n\n# How to contribute?\n\n# Future improvements and upcoming changes\n\n",
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
