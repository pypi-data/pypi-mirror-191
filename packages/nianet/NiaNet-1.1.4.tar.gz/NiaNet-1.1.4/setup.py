# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nianet']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'niapy>=2.0.4,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'torch>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'nianet',
    'version': '1.1.4',
    'description': 'Designing and constructing neural network topologies using nature-inspired algorithms',
    'long_description': '<p align="center"><img src=".github/NiaNetLogo.png" alt="NiaPy" title="NiaNet"/></p>\n\n---\n[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/nianet/)\n![PyPI - Python Version](https://img.shields.io/badge/python-3.8-blue)\n[![Downloads](https://static.pepy.tech/badge/nianet)](https://pepy.tech/project/nianet)\n[![GitHub license](https://img.shields.io/badge/license-MIT-green)](https://github.com/SasoPavlic/NiaNet/blob/main/LICENSE)\n### Designing and constructing neural network topologies using nature-inspired algorithms\n\n### Description 📝\n\nThe proposed method NiaNet attempts to pick hyperparameters and AE architecture that will result in a successful encoding and decoding (minimal difference between input and output). NiaNet uses the collection of algorithms available in the library [NiaPy](https://github.com/NiaOrg/NiaPy) to navigate efficiently in waste search-space.\n\n### What it can do? 👀\n\n* **Construct novel AE\'s architecture** using nature-inspired algorithms.\n* It can be utilized for **any kind of dataset**, which has **numerical** values.\n\n### Installation ✅\n\nInstalling NiaNet with pip3: \n```sh\npip3 install nianet\n```\n\n### Documentation 📘\n\n**Annals of Computer Science and Information Systems, Volume 30:**\n[NiaNet: A framework for constructing Autoencoder architectures using nature-inspired algorithms](https://www.sasopavlic.com/publication/nianet-a-framework-for-constructing-autoencoder-architectures-using-nat-ure-inspired-algorithms/)\n\n### Examples\n\nUsage examples can be found [here](examples).\n\n### Getting started 🔨\n\n##### Create your own example:\nIn [examples](examples) folder create the Python file based on the existing [evolve_for_diabetes_dataset.py](examples/evolve_for_diabetes_dataset.py).\n\n##### Change dataset:\nChange the dataset import function as follows:\n```python\nfrom sklearn.datasets import load_diabetes\ndataset = load_diabetes()\n```\n\n##### Specify the search space:\n\nSet the boundaries of your search space with [autoencoder.py](nianet/autoencoder.py).\n\nThe following dimensions can be modified:\n* Topology shape (symmetrical, asymmetrical)\n* Size of input, hidden and output layers\n* Number of hidden layers\n* Number of neurons in hidden layers\n* Activation functions\n* Number of epochs\n* Learning rate\n* Optimizer\n\nYou can run the NiaNet script once your setup is complete.\n##### Running NiaNet script:\n\n`python evolve_for_diabetes_dataset.py`\n\n### HELP ⚠️\n\n**saso.pavlic@student.um.si**\n\n## Acknowledgments 🎓\n\n* NiaNet was developed under the supervision\n  of [doc. dr Iztok Fister ml.](http://www.iztok-jr-fister.eu/)\n  at [University of Maribor](https://www.um.si/en/home-page/).\n\n* This code is a fork of [NiaPy](https://github.com/NiaOrg/NiaPy). I am grateful that the authors chose to\n  open-source their work for future use.\n\n# Cite us\nAre you using NiaNet in your project or research? Please cite us!\n### Plain format\n```\nS. Pavlič, I. F. Jr, and S. Karakatič, “NiaNet: A framework for constructing Autoencoder architectures using nature-inspired algorithms,” in Annals of Computer Science and Information Systems, 2022, vol. 30, pp. 109–116. Accessed: Oct. 08, 2022. [Online]. Available: https://annals-csis.org/Volume_30/drp/192.html\n```\n### Bibtex format\n```\n    @article{NiaPyJOSS2018,\n        author  = {Vrban{\\v{c}}i{\\v{c}}, Grega and Brezo{\\v{c}}nik, Lucija\n                  and Mlakar, Uro{\\v{s}} and Fister, Du{\\v{s}}an and {Fister Jr.}, Iztok},\n        title   = {{NiaPy: Python microframework for building nature-inspired algorithms}},\n        journal = {{Journal of Open Source Software}},\n        year    = {2018},\n        volume  = {3},\n        issue   = {23},\n        issn    = {2475-9066},\n        doi     = {10.21105/joss.00613},\n        url     = {https://doi.org/10.21105/joss.00613}\n    }\n```\n### RIS format\n```\nTY  - CONF\nTI  - NiaNet: A framework for constructing Autoencoder architectures using nature-inspired algorithms\nAU  - Pavlič, Sašo\nAU  - Jr, Iztok Fister\nAU  - Karakatič, Sašo\nT2  - Proceedings of the 17th Conference on Computer Science and Intelligence Systems\nC3  - Annals of Computer Science and Information Systems\nDA  - 2022///\nPY  - 2022\nDP  - annals-csis.org\nVL  - 30\nSP  - 109\nEP  - 116\nLA  - en\nSN  - 978-83-962423-9-6\nST  - NiaNet\nUR  - https://annals-csis.org/Volume_30/drp/192.html\nY2  - 2022/10/08/19:08:20\nL1  - https://annals-csis.org/Volume_30/drp/pdf/192.pdf\nL2  - https://annals-csis.org/Volume_30/drp/192.html\n```\n\n\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Sašo Pavlič',
    'author_email': 'saso.pavlic@student.um.si',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SasoPavlic/NiaNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
