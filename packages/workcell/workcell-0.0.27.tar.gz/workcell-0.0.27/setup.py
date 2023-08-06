# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workcell',
 'workcell.cli',
 'workcell.core',
 'workcell.deploy',
 'workcell.deploy.huggingface',
 'workcell.integrations.types',
 'workcell.templates.runtime.aws.custom.app',
 'workcell.templates.runtime.aws.python3.8',
 'workcell.templates.runtime.aws.python3.9',
 'workcell.templates.scaffold.huggingface.python3.8',
 'workcell.templates.scaffold.huggingface.python3.9',
 'workcell.templates.scaffold.weanalyze.python3.8',
 'workcell.templates.scaffold.weanalyze.python3.9',
 'workcell.utils']

package_data = \
{'': ['*'],
 'workcell': ['templates/frontend/*',
              'templates/runtime/aws/custom/*',
              'templates/runtime/huggingface/python3.8/*',
              'templates/runtime/huggingface/python3.9/*']}

install_requires = \
['altair>=4.2.2,<5.0.0',
 'colorama>=0.4.6,<0.5.0',
 'docker>=6.0.1,<7.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'huggingface-hub>=0.12.0,<0.13.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'mangum>=0.17.0,<0.18.0',
 'orjson>=3.8.6,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'perspective-python>=1.9.3,<2.0.0',
 'plotly>=5.12.0,<6.0.0',
 'poetry-bumpversion>=0.3.0,<0.4.0',
 'pyarrow>=11.0.0,<12.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'typer>=0.3.1,<0.4.0',
 'uvicorn>=0.18.3,<0.19.0']

entry_points = \
{'console_scripts': ['workcell = workcell.cli:cli']}

setup_kwargs = {
    'name': 'workcell',
    'version': '0.0.27',
    'description': 'Turn python function into microservice.',
    'long_description': '<!-- markdownlint-disable MD033 MD041 -->\n<h1 align="center">\n    Workcell\n</h1>\n\n<p align="center">\n    <strong>Instantly turn your Python function into production-ready microservice.</strong>\n</p>\n\n<p align="center">\n    <a href="https://pypi.org/project/workcell/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/workcell?color=green&style=flat"></a>\n    <a href="https://github.com/weanalyze/workcell/actions/workflows/release.yml" title="PyPi Version"><img src="https://github.com/weanalyze/workcell/actions/workflows/release.yml/badge.svg"></a> \n    <a href="https://github.com/weanalyze/workcell/actions/workflows/build-image.yml" title="PyPi Version"><img src="https://github.com/weanalyze/workcell/actions/workflows/build-image.yml/badge.svg"></a>     \n    <a href="https://pypi.org/project/workcell/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.8%2B-blue&style=flat"></a>\n    <a href="https://github.com/weanalyze/workcell/blob/main/LICENSE" title="Project License"><img src="https://img.shields.io/badge/License-Apache2.0-blue.svg"></a>\n    <a href="https://weanalyze.co">\n        <img alt="website" src="https://img.shields.io/website/https/weanalyze.co?down_color=red&down_message=offline&up_message=online">\n    </a>    \n    <a href="https://discord.gg/jZuDU5mQZ7">\n        <img alt="discord" src="https://img.shields.io/discord/1004913083812167811?label=discord">\n    </a>      \n</p>\n\n<h4 align="center">\n    <p>\n        <b>English</b> |\n        <a href="https://github.com/weanalyze/workcell/blob/main/README_zh-hans.md">简体中文</a> \n    <p>\n</h4>\n\n<p align="center">\n  <a href="#getting-started">Getting Started</a> •\n  <a href="#license">License</a> •\n  <a href="https://github.com/weanalyze/workcell/releases">Changelog</a>\n</p>\n\nInstantly turn your Python function into delightful app and production-ready microservice, with lightweight UI to interact with. \n\n<img align="center" style="width: 100%" src="https://github.com/weanalyze/weanalyze-resources/blob/main/assets/workcell_intro.png?raw=true"/>\n\n---\n\n## Highlights\n\n- 🔌  Instantly turn functions into microservices within seconds.\n- 📈  Automatically generate user-friendly UI for interaction.\n- 🤗  One-click deployment to Hugging Face Spaces.\n- ☁️  Develop locally, deploy to the cloud.\n- 🧩  Empower development and analysis with scalable components.\n- 🦄  Get inspired by the open-source community.\n\n## Status\n\n| Status | Stability | Goal |\n| ------ | ------ | ---- |\n| ✅ | Alpha | We are testing Workcell with a closed set of customers |\n| 🚧 | Public Alpha | Anyone can sign up over at weanalyze.co. But go easy on us, there are a few kinks. |\n| ❌ | Public Beta | Stable enough for most non-enterprise use-cases |\n| ❌ | Public | Production-ready |\n\nWe are currently in: **Alpha**. \n\n## Requirements\n\nPython 3.8+\n\n## Installation\n\nTo get started with Workcell, you can install it using `pip`:\n\nRecomended: First activate your virtual environment, with your favourite system. For example, we like poetry and conda!\n\n```bash\npip install workcell\n```\n\n## Getting Started\n\nHere is an example of a simple Workcell-compatible function:\n\n```python\nfrom pydantic import BaseModel\n\nclass Input(BaseModel):\n    message: str\n\nclass Output(BaseModel):\n    message: str\n\ndef hello_workcell(input: Input) -> Output:\n    """Returns the `message` of the input data."""\n    return Output(message=input.message)\n```\n\n_💡Note: A workcell-compatible function must have an `input` parameter and return value based on [Pydantic models](https://pydantic-docs.helpmanual.io/). The input and output models are specified using [type hints](https://docs.python.org/3/library/typing.html)._\n\nTo start a Workcell app, follow these steps:\n\n1. Copy the above code to a file named `app.py`.\n\n2. Create a folder, e.g. `hello_workcell`, and place the `app.py` inside.\n\n3. Open your terminal and navigate to the folder `hello_workcell`.\n\n4. Start the Workcell app using the following command: \n\n```bash\nworkcell serve app:hello_workcell\n```\n\n_💡Note: The output will display the location where the API is being served on your local machine._\n\nAlternatively, you can import the `workcell` package and serve your function using an ASGI web server such as [Uvicorn](http://www.uvicorn.org/) or [FastAPI](https://fastapi.tiangolo.com/). Simply wrap your function with `workcell.create_app` like this:\n\n```python\nfrom pydantic import BaseModel\nimport workcell\n\nclass Input(BaseModel):\n    message: str\n\nclass Output(BaseModel):\n    message: str\n\ndef hello_workcell(input: Input) -> Output:\n    """Returns the `message` of the input data."""\n    return Output(message=input.message)\n\napp = workcell.create_app(hello_workcell)\n```\n\nFinally, run the app using the following command:\n\n```bash\nuvicorn app:app --host 0.0.0.0 --port 7860\n```\n_💡Note: The output will display the location where the API is being served on your local machine._\n\n## Workcell deployment\n\n🤗 You can deploy your workcell to Hugging Face [Spaces](https://huggingface.co/spaces/launch) in 1-click! You\'ll be able to access your workcell from anywhere and share it with your team and collaborators.\n\n### **Prepare your Hugging Face account**\n\nFirst you need a Hugging Face account, and prepare your Hugging Face username and [User Access Tokens](https://huggingface.co/settings/tokens), then set environment variables like below:\n\n```bash\nexport HUGGINGFACE_USERNAME={huggingface_username}\nexport HUGGINGFACE_TOKEN={hf_XXX}\n```   \n\nReplace `{huggingface_username}` with your actual Hugging Face username, and `{hf_XXX}` with your actual User Access Token. You can also store these environment variables in a `.env` file in your project folder for convenience.\n\n### **Deploy Workcell**\n\n1. Wrap your function with `workcell.create_app` like example above.\n\n2. In your project folder, package your Workcell app using the following command:\n\n```bash\nworkcell pack app:hello_workcell\n```\n_💡Note: `workcell pack {file_name}:{create_app_name}` will package your function code with a `Dockerfile` template into `.workcell` folder in your project folder._\n\n3. Once packaged, deploy your Workcell app using the following command:\n\n```bash\nworkcell deploy\n```\n\nVoila! The deployment process will start, and within a few minutes, your workcell will be available on Hugging Face Spaces, accessible by a unique URL. \n\n### **More details**\n\nYou can monitor the deployment process and the logs in your terminal, and the deployment status will be shown in your Hugging Face Spaces repo.\n\nYou can deploy multiple workcells, and they will be listed in your Hugging Face Spaces account, you can manage and remove them from there.\n\nYou can also configure various deployment options like environment variables, system requirements, custom domain, etc., by using command line options or a `workcell_config.json` from `.workcell` dir in your project folder. \n\nPlease stay tuned, as a comprehensive guide will be available soon to provide further explanation.\n\n## Examples\n\n🎮 Get inspired and learn more about Workcell by exploring our examples:\n\n- https://github.com/weanalyze/workcell-examples\n\n🏆 We also have a curated list for you to check out, feel free to contribute!\n\n- https://github.com/weanalyze/best-of-workcell\n\n## Roadmap\n\n🗓️ Missing a feature? Have a look at our [public roadmap](https://github.com/orgs/weanalyze/projects/5/) to see what the team is working on in the short and medium term. Still missing it? Please let us know by opening an issue!\n\n## Contacts\n\n❓ If you have any questions about the workcell or weanalyze , feel free to email us at: support@weanalyze.co\n\n🙋🏻 If you want to say hi, or are interested in partnering with us, feel free to reach us at: contact@weanalyze.co\n\n😆 Feel free to share memes or any questions at Discord: https://discord.weanalyze.co\n\n## License\n\nApache-2.0 License.\n',
    'author': 'jiandong',
    'author_email': 'jiandong@weanalyze.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
