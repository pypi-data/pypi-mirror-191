# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'examples': './examples',
 'examples.csuite_example': './examples/csuite_example'}

packages = \
['causica',
 'causica.datasets',
 'causica.distributions',
 'causica.distributions.adjacency',
 'causica.distributions.noise_accessible',
 'causica.distributions.splines',
 'causica.functional_relationships',
 'causica.graph',
 'causica.lightning',
 'causica.sem',
 'causica.training',
 'examples',
 'examples.csuite_example']

package_data = \
{'': ['*']}

install_requires = \
['azureml-mlflow>=1.46.0,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'mlflow>=2.0.0,<3.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pytorch-lightning[extra]>=1.7.7,<2.0.0',
 'tensorboard>=2.9.0,<3.0.0',
 'tensordict>=0.0.2a0,<0.1.0',
 'types-PyYAML>=6.0.12.2,<7.0.0.0']

setup_kwargs = {
    'name': 'causica',
    'version': '0.1.1',
    'description': '',
    'long_description': '[![Causica CI Build](https://github.com/microsoft/causica/actions/workflows/ci-build.yml/badge.svg)](https://github.com/microsoft/causica/actions/workflows/ci-build.yml)\n\n# Causica\n\n## Overview\n \nCausal machine learning enables individuals and organizations to make better data-driven decisions. In particular, causal ML allows us to answer “what if” questions about the effect of potential actions on outcomes. \n \nCausal ML is a nascent area, we aim  to enable a **scalable**, **flexible**, **real-world applicable end-to-end** causal inference framework. In perticular, we bridge between causal discovery, causal inference, and deep learning to achieve the goal.  We aim to develop technology can automate causal decision-making using existing observational data alone, output both the discovered causal relationships and estimate the effect of actions simultaneously.\n \nCausica is a deep learning library for end-to-end causal inference, including both causal discovery and inference.  It implements deep end-to-end inference framework [2] and different alternatives.\n \nThis project splits the interventional decision making from observational decision making Azua repo found here [Azua](https://github.com/microsoft/project-azua).\n\nThis codebase has been heavily refactored, you can find the previous version of the code [here](https://github.com/microsoft/causica/releases/tag/v0.0.0).\n\n[1] Alvarez et al. [Simultaneous Missing Value Imputation and Structure Learning with Groups](https://openreview.net/pdf?id=4rm6tzBjChe), NeurIPS 2022\n\n[2] Geffner et al. [Deep End-to-end Causal Inference.](https://arxiv.org/pdf/2202.02195.pdf)\n\n[3] Gong et al.  [Rhino: Deep Causal Temporal Relationship Learning With History-dependent Noise](https://openreview.net/pdf?id=i_1rbq8yFWC), ICLR 2023\n\n[4] Ma et al. [Causal Reasoning in the Presence of Latent Confounders via Neural ADMG Learning]( https://openreview.net/pdf?id=dcN0CaXQhT), ICLR 2023\n\n# DECI: End to End Causal Inference\n\n## About\n\nReal-world data-driven decision making requires causal inference to ensure the validity of drawn conclusions. However, it is very uncommon to have a-priori perfect knowledge of the causal relationships underlying relevant variables. DECI allows the end user to perform causal inference without having complete knowledge of the causal graph. This is done by combining the causal discovery and causal inference steps in a single model. DECI takes in observational data and outputs ATE and CATE estimates. \n\nFor more information, please refer to the [paper](https://arxiv.org/abs/2202.02195).\n\n\n**Model Description**\n\nDECI is a generative model that employs an additive noise structural equation model (ANM-SEM) to capture the functional relationships among variables and exogenous noise, while simultaneously learning a variational distribution over causal graphs. Specifically, the relationships among variables are captured with flexible neural networks while the exogenous noise is modelled as either a Gaussian or spline-flow noise model. The SEM is reversible, meaning that we can generate an observation vector from an exogenous noise vector through forward simulation and given a observation vector we can recover a unique corresponding exogenous noise vector. In this sense, the DECI SEM can be seen as a flow from exogenous noise to observations. We employ a mean-field approximate posterior distribution over graphs, which is learnt together with the functional relationships among variables by optimising an evidence lower bound (ELBO). Additionally, DECI supports learning under partially observed data.\n\n**Simulation-based Causal Inference**\n\nDECI estimates causal quantities (ATE) by applying the relevant interventions to its learnt causal graph (i.e. mutilating incoming edges to intervened variables) and then sampling from the generative model. This process involves first sampling a vector of exogenous noise from the learnt noise distribution and then forward simulating the SEM until an observation vector is obtained. ATE can be computed via estimating an expectation over the effect variable of interest using MonteCarlo samples of the intervened distribution of observations. \n\n## How to run\n\nThe command to train this model the csuite_weak_arrows dataset and evaluate causal discovery and ATE estimation performance is:\n\n```\npython train_csuite_example.py --dataset csuite_weak_arrows\n```\n\nfrom within `examples/csuite_example`.\n\nThis will download the data from the CSuite Azure blob storage and train DECI on it. See [here](https://github.com/microsoft/csuite) for more info about CSuite datasets. The script will work on any of the available CSuite datasets.\n\nTo evaluate the model run:\n\n```\npython eval_csuite_example.py\n```\n\nThis should print various causal discovery and causal inference metrics.\n\n**Specifying a noise model**\n\nThe noise exogenous model can be modified by changing the `noise_dist` field within `training_default.json`, either \'gaussian\' or \'spline\' are allowed.\n\nThe Gaussian model has Gaussian exogenous noise distribution with mean set to 0 while its variance is learnt.\n\nThe Spline model uses a flexible spline flow that is learnt from the data. This model provides most gains in heavy-tailed noise settings, where the Gaussian model is at risk of overfitting to outliers, but can take longer to train.\n\n## Further extensions \n\nFor now, we have removed Rhino and DDECI from the codebase but they will be added back. You can still access the previously released versions [here](https://github.com/microsoft/causica/releases/tag/v0.0.0).\n\n# References\n\nIf you have used the models in our code base, please consider to cite the corresponding papers:\n\n[1], **(VISL)** Pablo Morales-Alvarez, Wenbo Gong, Angus Lamb, Simon Woodhead, Simon Peyton Jones, Nick Pawlowski, Miltiadis Allamanis, Cheng Zhang, "Simultaneous Missing Value Imputation and Structure Learning with Groups", [ArXiv preprint](https://arxiv.org/abs/2110.08223)\n\n[2], **(DECI)** Tomas Geffner, Javier Antoran, Adam Foster, Wenbo Gong, Chao Ma, Emre Kiciman, Amit Sharma, Angus Lamb, Martin Kukla, Nick Pawlowski, Miltiadis Allamanis, Cheng Zhang. Deep End-to-end Causal Inference. [Arxiv preprint](https://arxiv.org/abs/2202.02195) (2022)\n\n[3], **(DDECI)** Matthew Ashman, Chao Ma, Agrin Hilmkil, Joel Jennings, Cheng Zhang. Causal Reasoning in the Presence of Latent Confounders via Neural ADMG Learning. [ICLR](https://openreview.net/forum?id=dcN0CaXQhT) (2023)\n\n[4], **(Rhino)** Wenbo Gong, Joel Jennings, Cheng Zhang, Nick Pawlowski. Rhino: Deep Causal Temporal Relationship Learning with History-dependent Noise. [ICLR](https://openreview.net/forum?id=i_1rbq8yFWC) (2023)\n\nOther references:\n- Louizos, Christos, et al. "Causal effect inference with deep latent-variable models." Advances in neural information processing systems 30 (2017).\n- Hill, Jennifer L. "Bayesian nonparametric modeling for causal inference." Journal of Computational and Graphical Statistics 20.1 (2011): 217-240.\n\n\n# Development\n\n## Poetry\n\nWe use Poetry to manage the project dependencies, they\'re specified in the [pyproject.toml](pyproject.toml). To install poetry run:\n\n```\n    curl -sSL https://install.python-poetry.org | python3 -\n```\n\nTo install the environment run `poetry install`, this will create a virtualenv that you can use by running either `poetry shell` or `poetry run {command}`. It\'s also a virtualenv that you can interact with in the normal way too.\n\nMore information about poetry can be found [here](https://python-poetry.org/)\n\n## mlflow\n\nWe use [mlflow](https://mlflow.org/) for logging metrics and artifacts. By default it will run locally and store results in `./mlruns`.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
