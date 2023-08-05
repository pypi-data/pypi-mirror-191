# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pureml',
 'pureml.cli',
 'pureml.components',
 'pureml.config',
 'pureml.decorators',
 'pureml.deploy',
 'pureml.lineage',
 'pureml.lineage.data',
 'pureml.packaging',
 'pureml.packaging.model_packaging',
 'pureml.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'PyJWT>=2.4.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'docker>=6.0.1,<7.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyarrow>=8.0.0,<9.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['pureml = pureml.cli.main:app']}

setup_kwargs = {
    'name': 'pureml',
    'version': '0.2.0',
    'description': '',
    'long_description': '<h1 align="center">\n  <a href="https://pureml.com">\n    <img\n      align="center"\n      alt="PureML"\n      src="https://github.com/PureML-Inc/PureML/blob/main/assets/coverImg.jpeg"\n      style="width:100%;"\n    />\n  </a>\n</h1>\n\n\n\n\n<div align="center">\n\n# Track, version, compare and review your data and models.\n\n</div>\n\n\n# ⛳ Quick Access\n\n<p align="center">\n  <a\n    href="https://docs.pureml.com"\n  ><b>Documentation</b></a>\n  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;\n  <a\n    href="https://www.youtube.com/watch?v=HdzLFEWS4s8&t=1s"\n  ><b>Watch Demo</b></a>\n  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;\n  <a\n    href="https://docs.pureml.com/docs/get-started/quickstart_tabular"\n  ><b>Quick example</b></a>\n  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;\n  <a\n    href="#"\n  ><b>Get Instant Help</b></a>\n  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;\n  <a\n    href="https://app.pureml.com/auth/signup"\n  ><b>Sign Up for free</b></a>\n\n</p>\n\n\n\n</br>\n</br>\n\n\n<div align="center">\n  <a\n    href="https://pypi.org/project/pureml/"\n  >\n    <img alt="PyPi" src="https://img.shields.io/pypi/v/pureml?color=green&logo=pureml" />\n  </a>\n  &nbsp;\n  <a\n    href="https://python-poetry.org/"\n  >\n    <img src="https://img.shields.io/badge/poetry-1.1.14-blue?style=flat&logo=poetry&logoColor=white" />\n  </a>\n  &nbsp;\n  <a\n    href="https://opensource.org/licenses/Apache-2.0"\n  >\n    <img alt="License" src="https://img.shields.io/pypi/l/pureml?color=red&logo=Apache&logoColor=red" />\n  </a>\n  &nbsp;\n  <a\n    href="https://discord.gg/xNUHt9yguJ"\n  >\n    <img alt="Discord" src="https://img.shields.io/badge/Discord-Join%20Discord-blueviolet?style=flat&logo=discord&logoColor=white" />\n  </a>\n  &nbsp;\n  <a\n    href="https://pepy.tech/project/pureml"\n  >\n    <img alt="Downloads" src="https://static.pepy.tech/badge/pureml">\n  </a>\n  &nbsp;\n  <a\n    href="https://pypi.org/project/pureml/"\n  >\n    <img alt="^3.8" src="https://img.shields.io/pypi/pyversions/pureml">\n  </a>\n  &nbsp;\n  <a\n    href="https://pypi.org/project/pureml/"\n  >\n    <img alt="Coverage" src="https://img.shields.io/codecov/c/github/PureML-Inc/pureml">\n  </a>\n  &nbsp;\n  <a\n    href="https://pypi.org/project/pureml/"\n  >\n    <img alt="Coverage" src="https://img.shields.io/github/stars/pureml-inc/pureml?style=social">\n  </a>\n\n\n\n</div>\n\n\n</br>\n</br>\n\n\n\n# 💎 Intro\n\nPureML is an open-source version control for machine learning.\n\n1. [Quick start](#quick-start)\n1. [How it works](#how-it-works)\n1. [Demo](#demo)\n1. [Main Features](#main-features)\n1. [Core design principles](#core-design-principles)\n1. [Core abstractions](#core-abstractions)\n1. [Why to get involved](#why-to-get-involved)\n1. [Tutorials](#tutorials)\n\n<br />\n\n# ⏱ Quick start\n\nYou can install and run PureML using `pip`.\n\n\nInstall PureML\n```bash\npip install pureml\n```\n\n<br />\n\n# 📋 How it works\nJust add a few lines of code. You don\'t need to change the way you work.\n\nPureML is a Python library that uploads metadata to S3.\n\n### Generating Data Lineage\n\n1. Load Data\n```python\n@load_data(name=\'loading data\')\ndef loading_data():\n    \n    return pd.read_csv(\'churn.csv\')\n```\n\n2. Transform Data\n```python\n@transformer(name=\'fill missing values\')\ndef fill_missing_values(df):\n    return df.fillna()\n    \n\n@transformer(name=\'encode ordinal\')\ndef encode_ordinal(df):\n    col_ord = [\'state\', \'phone number\']\n    df_ord = df[col_ord]\n    feat = OrdinalEncoder().fit_transform(df_ord)    \n    df[col_ord] = feat\n    \n    return df\n\n@transformer(name=\'encode binary\')\ndef encode_binary(df):\n\n    df[\'voice mail plan\'] = df[\'voice mail plan\'].map({\'yes\':1, \'no\':0})\n    df[\'international plan\'] = df[\'international plan\'].map({\'yes\':1, \'no\':0})\n    df[\'churn\'] = df[\'churn\'].map({True:1, False:0})\n\n    return df\n```\n\n3. Register Dataset\n```python\n@dataset(name=\'telecom churn\', parent=\'encode binary\')\ndef build_dataset():\n    df = loading_data()\n\n    df = fill_missing_values(df)\n\n    df = encode_ordinal(df)\n\n    df = encode_binary(df)\n\n    return df\n\ndf = build_dataset()\n```\n\nThis is how generated data lineage will look like in the UI\n\n<h1 align="center">\n    <img\n      align="center"\n      src="https://github.com/PureML-Inc/PureML/blob/main/assets/pipeline.png?raw=true"\n      style="width:60%;"\n    />\n  </a>\n</h1>\n\nFor more detailed explanation, please visit our [Documentation](https://docs.pureml.com)\n\n# 💻 Demo\n\n### Live demo\n\nBuild and run a PureML project to create data lineage and a model with our <b>[demo colab link](https://colab.research.google.com/drive/1LlrpaKiREwgesaRcnwkJP-w2MPesXf1t?usp=sharing)</b>.\n\n\n### Demo video (2 min)\nPureML quick start demo\n\n[![PureML Demo Video](https://img.youtube.com/vi/HdzLFEWS4s8/0.jpg)](https://www.youtube.com/watch?v=HdzLFEWS4s8 "PureML Demo Video")\n\n\n\n<sub><i>Click the image to play video</i></sub>\n\n<br />\n\n\n# 📍 [Main Features](https://docs.pureml.com/)\n|   |   |\n| --- | --- |\n| Data Lineage | Automatic generation of data lineage|\n| Dataset Versioning | Object-based Automatic Semantic Versioning of datasets |\n| Model Versioning | Object-based Automatic Semantic Versioning of models |\n| Comparision | Comparing different versions of models or datasets\n| Branches (*Coming Soon*) | Separation between experimentation and production ready models using branches |\n| Review (*Coming Soon*) | Review and approve models, and datasets to production ready branch|\n\n<br />\n\n\n# 🔮 Core design principles\n\n|   |   |\n| --- | --- |\n| Easy developer experience | An intuitive open source package aimed to bridge the gaps in data science teams |\n| Engineering best practices built-in | Integrating PureML functionalities in your code doesnot disrupt your workflow |\n| Object Versioning | A reliable object versioning mechanism to track changes to your datasets, and models |\n| Data is a first-class citizen | Your data is secure. It will never leave your system. |\n| Reduce Friction | Have access to operations performed on data using data lineage without having to spend time on lengthy meetings |\n\n\n\n<br />\n\n# ⚙ Core abstractions\n\nThese are the fundamental concepts that PureML uses to operate.\n\n|   |   |\n| --- | --- |\n| [Project](https://docs.pureml.com/docs/projects/about_projects) | A data science project. This is where you store datasets, models, and their related objects. It is similar to a github repository with object storage.|\n| [Lineage](https://docs.pureml.com/docs/data/register_data_pipeline) | Contains a series of transformations performed on data to generate a dataset.|\n| Data Versioning | Versioning of the data should be comprehensible to the user and should encapsulate the changes in the data, its creation mechanism, among others.|\n| Model Versioning| Versioning of the model should be comprehensible to the user and should encapuslate the changes in training data, model architecture, hyper parameters.|\n| Fetch | This functionality is used to fetch registered Models, and Datasets.|\n\n\n<br />\n\n# 🤝 Why to get involved\nVersion control is much more common in software than in machine learning. So why isn’t everyone using Git? Git doesn’t work well with machine learning. It can’t handle large files, it can’t handle key/value metadata like metrics, and it can’t record information automatically from inside a training script.\n\nGitHub wasn’t designed with data as a core project component. This along with a number of other differences between AI and more traditional software projects makes GitHub a bad fit for artificial intelligence, contributing to the reproducibility crisis in machine learning.\n\nFrom manually tracking models to git based versioning systems that do not follow an intuitive versioning mechanism, there is no standardized way to track objects. Using these mechanisms, it is hard enough to track or get your model from a month ago running, let alone of a teammates!\n\nWe are trying to build a version control system for machine learning objects. A mechanism that is object dependant and intuitive for users.\n\nLets build this together. If you have faced this issue or have worked out a similar solution for yourself, please join us to help build a better system for everyone.\n\n<br />\n\n\n# 🧮 Tutorials\n\n- [Registering Data lineage](https://docs.pureml.com/docs/data/register_data_pipeline)\n- [Registering models](https://docs.pureml.com/docs/models/register_models)\n- [Quick Start: Tabular](https://docs.pureml.com/docs/get-started/quickstart_tabular)\n- [Quick Start: Computer Vision](https://docs.pureml.com/docs/get-started/quickstart_cv)\n- [Quick Start: NLP](https://docs.pureml.com/docs/get-started/quickstart_nlp)\n- [Logging](https://docs.pureml.com/docs/log/overview)\n\n\n<br />\n\n# 🐞 Reporting Bugs\nTo report any bugs you have faced while using PureML package, please\n1. Report it in [Discord](https://discord.gg/xNUHt9yguJ) channel\n1. Open an [issue](https://github.com/PureML-Inc/PureML/issues)\n\n<br />\n\n# ⌨ Contributing and Developing\nLets work together to improve the features for everyone. For more details, please look at out [Contributing Guide](./CONTRIBUTING.md)\n\nWork with mutual respect.\n\n\n<br />\n\n# 👨\u200d👩\u200d👧\u200d👦 Community\nTo get quick updates, feature release for PureML follow us on\n|   |\n| --- |\n| [<img alt="Twitter" height="20" src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />](https://twitter.com/getPureML) |\n[<img alt="LinkedIn" height="20" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/company/pureml-inc/) |\n| [<img alt="GitHub" height="20" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />](https://github.com/PureML-Inc/PureML) |\n| [<img alt="GitHub" height="20" src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" />](https://discord.gg/DBvedzGu) |\n\n\n# 📄 License\nSee the [Apache-2.0](./License) file for licensing information.\n\n\n\n<br />\n',
    'author': 'vamsidhar muthireddy',
    'author_email': 'vamsi.muthireddy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pureml.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
