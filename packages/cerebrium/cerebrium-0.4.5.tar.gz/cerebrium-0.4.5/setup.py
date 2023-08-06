# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cerebrium', 'cerebrium.logging', 'cerebrium.models']

package_data = \
{'': ['*']}

install_requires = \
['arize>=6.0.2,<7.0',
 'censius>=1.6,<2.0',
 'cloudpickle>=2.0,<2.1',
 'numpy>=1.24,<1.25',
 'onnxruntime>=1.13,<1.14',
 'pandas>=1.5,<1.6',
 'requests>=2.28,<2.29',
 'scikit-learn>=1.2,<1.3',
 'tenacity>=8.2,<8.3',
 'torch>=1.13,<1.14',
 'tqdm>=4.64,<4.65',
 'xgboost>=1.7,<1.8',
 'yaspin>=2.3,<2.4']

setup_kwargs = {
    'name': 'cerebrium',
    'version': '0.4.5',
    'description': '',
    'long_description': '# Cerebrium\n\nCerebrium is the Python package built for use with the [Cerebrium](https://www.cerebrium.ai/) platform, which allows you to deploy your machine learning models as a REST API with a single line of code.\n\nFor usage consult the [documentation](https://docs.cerebrium.ai/). The repo for the documentation can be found [here](https://github.com/CerebriumAI/docs).\n\n# Development environment\nCerebrium uses Poetry for dependency management and packaging. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Alternatively, consult our article on [how to manage your python environments](https://blog.cerebrium.ai/setting-up-your-data-science-and-ml-development-environment-949277339939?gi=54b980dd4e1d).\n\nYou can run the following steps to setup your Python development environment with the following commands:\n```bash\npoetry install\npoetry shell\n```\nYou should use this environment to run tests, notebooks and build the package.\n\nFurthermore, you should set up a `.env` file in the project root with the following environment variables:\n```bash\nDEVELOPMENT_ENV=dev\n```\n\nYou can add packages to the project by running the following command:\n```bash\npoetry add <package>\n```\n\nYou **will** need to relock if you have added any packages to the project. You can do this by running the following command:\n```bash\npoetry lock\n```\n\n## Codespaces Setup\nTo set up a Codespaces for development, you should run the following command to setup AWS:\n```bash\ncd ~\ncurl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"\nunzip awscliv2.zip\nsudo ./aws/install\n```\n\n## Running tests\nTo run the tests, run the following command:\n```bash\npoetry run pytest --cov-report html:cov_html\\\n          --cov-report annotate:cov_annotate\\\n          --cov=cerebrium tests/\n```\n\n## Publishing Development Builds\nTo publish a development build on CodeArtifact, run the following command to configure Poetry:\n```bash\npoetry config http-basic.cerebrium aws $(aws codeartifact get-authorization-token --domain-owner 288552132534 --domain cerebrium --query \'authorizationToken\' --output text --region eu-west-1)\n```\n\nThen, run the following command to publish the package:\n```bash\npoetry shell # this is needed to set the version dynamically\npoetry publish --build -r cerebrium\n```\n\nIf the patch version is not up to date, merge the latest version tag into the branch:\n```bash\ngit merge v<tag>\n```\n\n## Install a development build\nTo install a development build, run the following command to configure pip:\n```bash\n\naws codeartifact login --tool pip --repository cerebrium-pypi --domain cerebrium --domain-owner 288552132534 --region eu-west-1\n```\nThen, pip install:\n```bash\npip install --pre cerebrium\n```\n\n## Exporting Requirements for Cerebrium Server\nYou should export the requirements for the Cerebrium server by running the following command:\n```bash\npoetry export >> cerebrium-requirements.txt\n```\nOnce this is done, add them to the `cerebrium-conduit-server` repo.\n\n### Resources for Poetry/CodeArtifact\n- https://repost.aws/questions/QURD7aFNj_R9-8odJY5mfgrw/npm-publish-for-a-package-to-aws-code-artifact-repo-fails-with-error-the-provided-package-is-configured-to-block-new-version-publishes\n- https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-pip.html',
    'author': 'Elijah Roussos',
    'author_email': 'elijah@cerebrium.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
