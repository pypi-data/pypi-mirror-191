# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_sklearn', 'neptune_sklearn.impl']

package_data = \
{'': ['*']}

install_requires = \
['neptune-client>=0.16.17',
 'scikit-learn>=0.24.1',
 'scikit-plot>=0.3.7',
 'yellowbrick>=1.3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'neptune-sklearn',
    'version': '2.0.0',
    'description': 'Neptune.ai scikit-learn integration library',
    'long_description': '# Neptune + Scikit-learn Integration\n\nExperiment tracking, model registry, data versioning, and live model monitoring for Scikit-learn (Sklearn) trained models.\n\n## What will you get with this integration?\n\n* Log, display, organize, and compare ML experiments in a single place\n* Version, store, manage, and query trained models, and model building metadata\n* Record and monitor model training, evaluation, or production runs live\n\n## What will be logged to Neptune?\n\n* classifier and regressor parameters,\n* pickled model,\n* test predictions,\n* test predictions probabilities,\n* test scores,\n* classifier and regressor visualizations, like confusion matrix, precision-recall chart, and feature importance chart,\n* KMeans cluster labels and clustering visualizations,\n* metadata including git summary info.\n* [other metadata](https://docs.neptune.ai/you-should-know/what-can-you-log-and-display)\n\n![image](https://user-images.githubusercontent.com/97611089/160642485-afca99da-9f7b-4d80-b0be-810c9d5770e5.png)\n*Confusion matrix logged to Neptune*\n\n\n## Resources\n\n* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/model-training/sklearn)\n* [Code example on GitHub](https://github.com/neptune-ai/examples/blob/main/integrations-and-supported-tools/sklearn/scripts/Neptune_Scikit_learn_classification.py)\n* [Runs logged in the Neptune app](https://app.neptune.ai/o/common/org/sklearn-integration/e/SKLEAR-95/all)\n* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/master/integrations-and-supported-tools/sklearn/notebooks/Neptune_Scikit_learn.ipynb)\n\n## Example\n\n```python\n# On the command line:\npip install scikit-learn neptune-client neptune-sklearn\n```\n```python\n# In Python, prepare a fitted estimator\nparameters = {"n_estimators": 70,\n              "max_depth": 7,\n              "min_samples_split": 3}\n\nestimator = ...\nestimator.fit(X_train, y_train)\n\n# Import Neptune and start a run\nimport neptune.new as neptune\nrun = neptune.init_run(project="common/sklearn-integration",\n                   api_token="ANONYMOUS")\n\n\n# Log parameters and scores\nrun["parameters"] = parameters\n\ny_pred = estimator.predict(X_test)\n\nrun["scores/max_error"] = max_error(y_test, y_pred)\nrun["scores/mean_absolute_error"] = mean_absolute_error(y_test, y_pred)\nrun["scores/r2_score"] = r2_score(y_test, y_pred)\n\n\n# Stop the run\nrun.stop()\n```\n\n## Support\n\nIf you got stuck or simply want to talk to us, here are your options:\n\n* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions)\n* You can submit bug reports, feature requests, or contributions directly to the repository.\n* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),\n* You can just shoot us an email at support@neptune.ai\n',
    'author': 'neptune.ai',
    'author_email': 'contact@neptune.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://neptune.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
