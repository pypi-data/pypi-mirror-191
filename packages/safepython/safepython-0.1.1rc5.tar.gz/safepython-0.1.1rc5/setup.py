# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safepython']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=2.2.3', 'numba>=0.49.0', 'numpy>=1.19.2', 'scipy>=1.3.0']

setup_kwargs = {
    'name': 'safepython',
    'version': '0.1.1rc5',
    'description': 'A Python implementation of the SAFE toolbox for sensitivity analysis',
    'long_description': '# SAFEpython\nPython version of the Sensitivity Analysis for Everybody (SAFE) Toolbox.\n\n[![License: GPL-3.0](https://img.shields.io/badge/License-GPL3.0-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)\n\n<p align="center">\n<img src="https://raw.githubusercontent.com/SAFEtoolbox/SAFEtoolbox.github.io/main/drawing2.png" width = "300px">\n</p>\n\n### BEFORE STARTING\n\nAn introduction to the SAFE Toolbox is provided in the paper:\n\nPianosi, F., Sarrazin, F., Wagener, T. (2015), A Matlab toolbox for Global Sensitivity Analysis, Environmental Modelling & Software, 70, 80-85. The paper is freely available at: https://doi.org/10.1016/j.envsoft.2015.04.009\n\nWe recommend reading this (short) paper before getting started. Other reading materials, including general introductions to Sensitivity Analysis and case study applications, can be found at: https://safetoolbox.github.io\n\n### INSTALLING THE PACKAGE\n\n#### Option 1: Installing the package using pip\n\n``pip install SAFEpython``\n\n#### Option 2: Installing a local version of the package (if you want to customize the code)\n\nDownload the SAFEpython source code to your computer. You go into the SAFE-Python folder and execute: \n\n``pip install .``\n\n#### Notes\n\n- You can execute the previous commands from python command line (e.g. Anaconda prompt). \n\n- From command line, you should use:\n\noption 1: ``python -m pip install SAFEpython``\n\t\noption 2: ``python -m pip install .``\n\n- For windows users: python cannot be called directly from Windows command line. You have to go into the folder in which python is installed and then execute:\n\noption 1: ``python -m pip install SAFEpython``\n\t\noption 2: ``python -m pip install mydir\\SAFE-python``\n\n(mydir is the directory in which the SAFEpython folder is saved, and it shoud not contain which spaces)\n\n\n- If you want to install the package without administrator rights, you may have to use:\n\t\n``pip install --user .``\n\n\n### GETTING STARTED\n\nTo get started using SAFE, we suggest opening one of the workflow scripts in the \'examples\' folder available in the [**_github repository_**](https://github.com/SAFEtoolbox/SAFE-python) and running the code step by step. The header of each workflow script gives a short description of the method and case study model, and of the main steps and purposes of that workflow, as well as references for further reading. The name of each workflow is composed as: workflow_method_model\n\nImplemented models are:\n- the hydrological Hymod model \n- the hydrological HBV model \n- the Ishigami and Homma test function \n- the Sobol\' g-function \n\nImplemented methods are:\n- eet (elementary effects test, or method of Morris)\n- fast (Fourier amplitude sensitivity test)\n- pawn\n- rsa (regional sensitivity analysis)\n- vbsa (variance-based sensitivity analysis, or method of Sobol\')\n\nFurthermore, SAFE includes additional workflow scripts:\n- external: how to connect SAFE to a model running outside python\n- tvsa: how to apply GSA methods to perform time-varying sensitivity analysis \n- visual: how to use visualisation functions for qualitative GSA\n\nIf the user still has no clear idea of what method(s) to start with, we suggest one of the three most widely used methods: eet (e.g. workflow_eet_hymod), rsa (workflow_rsa_hymod), vbsa (workflow_vbsa_hymod) or the visualization workflow (workflow_visual_ishigami_homma.m).\n\n### Note \n\nPlease make sure that you download the version of the \'examples\' folder that corresponds to the version of SAFEypthon package you are using. To use the latest version of SAFEpython, you can update the package using: \n\n``pip install --upgrade SAFEpython``\n\n### HOW TO CITE SAFEPYTHON\n\nIf you would like to use the software, please cite it using the following:\n\nPianosi, F., Sarrazin, F., Wagener, T. (2015), A Matlab toolbox for Global Sensitivity Analysis, Environmental Modelling & Software, 70, 80-85, doi: 10.1016/j.envsoft.2015.04.009.\n\n[![DOI](https://img.shields.io/badge/doi.org/10.1016/j.envsoft.2015.04.009-purple.svg)](https://doi.org/10.1016/j.envsoft.2015.04.009)\n',
    'author': 'Francesca Pianosi, Fanny Sarrazin, Thorsten Wagener',
    'author_email': 'fanny.sarrazin@ufz.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SAFEtoolbox/SAFE-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
