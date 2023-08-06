# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyreal',
 'pyreal.applications',
 'pyreal.benchmark',
 'pyreal.benchmark.challenges',
 'pyreal.benchmark.challenges.gfi',
 'pyreal.benchmark.challenges.lfc',
 'pyreal.explainers',
 'pyreal.explainers.dte',
 'pyreal.explainers.gfi',
 'pyreal.explainers.lfc',
 'pyreal.explainers.time_series',
 'pyreal.explainers.time_series.saliency',
 'pyreal.transformers',
 'pyreal.types',
 'pyreal.types.explanations',
 'pyreal.utils']

package_data = \
{'': ['*'],
 'pyreal.applications': ['data/*'],
 'pyreal.benchmark': ['models/*',
                      'results/20210916-115944/*',
                      'results/20210924-133808/*']}

install_requires = \
['eli5>=0.11,<0.14',
 'lime>=0.2.0.1,<0.3.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'shap==0.40.0']

extras_require = \
{'examples': ['tensorflow>=2.6.0,<=2.10.0', 'lightgbm>=3.3.2,<4.0.0']}

setup_kwargs = {
    'name': 'pyreal',
    'version': '0.3.2',
    'description': 'Library for evaluating and deploying human readable machine learning explanations.',
    'long_description': '<p align="left">\n<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt=“DAI-Lab” />\n<i>An open source project from Data to AI Lab at MIT.</i>\n</p>\n\n<!-- Uncomment these lines after releasing the package to PyPI for version and downloads badges -->\n[![PyPI Shield](https://img.shields.io/pypi/v/pyreal.svg)](https://pypi.python.org/pypi/pyreal)\n<!--[![Downloads](https://pepy.tech/badge/pyreal)](https://pepy.tech/project/pyreal)-->\n<!--[![Travis CI Shield](https://travis-ci.org/DAI-Lab/pyreal.svg?branch=stable)](https://travis-ci.org/DAI-Lab/pyreal)-->\n<!--[![Coverage Status](https://codecov.io/gh/DAI-Lab/pyreal/branch/stable/graph/badge.svg)](https://codecov.io/gh/DAI-Lab/pyreal)-->\n[![Build Action Status](https://github.com/DAI-Lab/pyreal/workflows/Test%20CI/badge.svg)](https://github.com/DAI-Lab/pyreal/actions)\n# Pyreal\n\nLibrary for evaluating and deploying machine learning explanations.\n\n- License: MIT\n- Documentation: https://pyreal.gitbook.io/pyreal\n- API Documentation: https://sibyl-ml.dev/pyreal/api_reference/index.html\n- Homepage: https://sibyl-ml.dev/\n\n# Overview\n\n**Pyreal** wraps the complete machine learning explainability pipeline into Explainer objects. Explainer objects\nhandle all the transforming logic, in order to provide a human-interpretable explanation from any original\ndata form.\n\n# Install\n\n## Requirements\n\n**Pyreal** has been developed and tested on [Python 3.8, 3.9, and 3.10](https://www.python.org/downloads/)\nThe library uses Poetry for package management.\n\n## Install from PyPI\n\nWe recommend using\n[pip](https://pip.pypa.io/en/stable/) in order to install **Pyreal**:\n\n```\npip install pyreal\n```\n\nThis will pull and install the latest stable release from [PyPI](https://pypi.org/).\n\n## Install from source\nIf you do not have **poetry** installed, please head to [poetry installation guide](https://python-poetry.org/docs/#installation)\nand install poetry according to the instructions.\\\nRun the following command to make sure poetry is activated. You may need to close and reopen the terminal.\n\n```\npoetry --version\n```\n\nFinally, you can clone this repository and install it from\nsource by running `poetry install`:\n\n```\ngit clone git@github.com:DAI-Lab/pyreal.git\ncd pyreal\npoetry install\n```\n\n## Install for Development\n\nIf you want to contribute to the project, a few more steps are required to make the project ready\nfor development.\n\nPlease head to the [Contributing Guide](https://sibyl-dev.github.io/pyreal/developer_guides/contributing.html)\nfor more details about this process.\n\n# Quickstart\n\nIn this short tutorial we will guide you through a series of steps that will help you\ngetting started with **Pyreal**. We will get an explanation for a prediction on whether a\npassenger on the Titanic would have survived.\n\n For a more detailed version of this tutorial, see\n`examples.titanic.titanic_lfc.ipynb`\n\n#### Load in demo dataset, pre-fit model, and transformers\n```\n>>> import pyreal.applications.titanic as titanic\n>>> from pyreal.transformers import ColumnDropTransformer, MultiTypeImputer\n\n# Load in data\n>>> x_train_orig, y = titanic.load_titanic_data()\n\n# Load in feature descriptions -> dict(feature_name: feature_description, ...)\n>>> feature_descriptions = titanic.load_feature_descriptions()\n\n# Load in model\n>>> model = titanic.load_titanic_model()\n\n# Load in list of transformers\n>>> transformers = titanic.load_titanic_transformers()\n\n# Create and fit LocalFeatureContribution Explainer object\n>>> from pyreal.explainers import LocalFeatureContribution\n>>> lfc = LocalFeatureContribution(model=model, x_train_orig=x_train_orig,\n...                                transformers=transformers,\n...                                feature_descriptions=feature_descriptions,\n...                                fit_on_init=True)\n\n# Make predictions on an input\n>>> input_to_explain = x_train_orig.iloc[0]\n>>> prediction = lfc.model_predict(input_to_explain) # Prediction: [0]\n\n# Explain an input\n>>> contributions = lfc.produce(input_to_explain)\n\n# Visualize the explanation\n>>> from pyreal.utils import visualize\n>>> x_interpret = lfc.convert_data_to_interpretable(input_to_explain)\n\n```\n\n<!--## Install for Development\n\nTODO: Running tests should not bring up a window. Refactor into the above docstring, not actually spawning the subsequent window-->\n\n##### Plot a bar plot of top contributing features, by absolute value\n```\nvisualize.plot_top_contributors(contributions, select_by="absolute", values=x_interpret)\n```\n\n\nThe output will be a bar plot showing the most contributing features, by absolute value.\n\n![Quickstart](docs/images/quickstart.png)\n\nWe can see here that the input passenger\'s predicted chance of survival was greatly reduced\nbecause of their sex (male) and ticket class (3rd class).\n\n### Terminology\nPyreal introduces specific terms and naming schemes to refer to different feature spaces and\ntransformations. The [Terminology User Guide](https://sibyl-ml.dev/pyreal/user_guides/transformer_workflow.html#terminology) provides an introduction to these terms.\n\n# What\'s next?\n\nFor more details about **Pyreal** and all its possibilities\nand features, please check the [documentation site](\nhttps://sibyl-dev.github.io/pyreal/).\n',
    'author': 'Alexandra Zytek',
    'author_email': 'zyteka@mit.edu',
    'maintainer': 'MIT Data To AI Lab',
    'maintainer_email': 'dailabmit@gmail.com',
    'url': 'https://sibyl-ml.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
