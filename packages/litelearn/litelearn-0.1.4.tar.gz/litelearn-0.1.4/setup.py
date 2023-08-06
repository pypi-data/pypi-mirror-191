# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['litelearn']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.1.1,<2.0.0',
 'ipython>=7.9.0,<8.0.0',
 'numpy>=1.21.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'shap>=0.41.0,<0.42.0']

setup_kwargs = {
    'name': 'litelearn',
    'version': '0.1.4',
    'description': 'a python library for quickly building and evaluating models',
    'long_description': '# litelearn\n\na python library for building models without fussing\nover the nitty gritty details for data munging\n\nonce you have a `pandas` dataframe you can create a model \nfor your dataset in 3 lines of code:\n\n```python\n# load some dataset\nimport seaborn as sns\ndataset = "penguins"\ntarget = "body_mass_g"\ndf = sns.load_dataset(dataset).dropna(subset=[target])\n\n# just 3 lines of code to create \n# and evaluate a model\nimport litelearn as ll\nmodel = ll.core_regress_df(df, target)\nresult = model.get_evaluation() \n```\n\n## installation\n`pip install litelearn`',
    'author': 'Aviad Rozenhek',
    'author_email': 'aviadr1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.15,<3.11',
}


setup(**setup_kwargs)
