# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nemglo', 'nemglo.backend', 'nemglo.components', 'nemglo.planning']

package_data = \
{'': ['*']}

install_requires = \
['flask-cors>=3.0.10,<4.0.0',
 'flask>=2.2.2,<3.0.0',
 'mip>=1.13.0,<2.0.0',
 'nemed',
 'nemosis>=3.1.0,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'nemglo',
    'version': '0.2.2',
    'description': 'Green-energy Load Optimisation tool for the NEM',
    'long_description': '# NEMGLO\nNEMGLO, the Green-energy Load Optimisation tool for the Australian National Electricity Market (NEM) is a python tool allows users to counterfactually assess flexible load operating strategies in the NEM using historical market data. Specifically, the tool enables users to test various scenarios with differing PPA contracting structures and green-certificate schemes, a primary case study being the ability to \'validate\' the integrity of "green"-hydrogen produced via grid-connected electrolysis with bundled PPA contracting. Although the tool was developed contextually for electrolyser loads, the functionalities can inherently be abstracted to commercial/industrial flexible loads seeking to consume green-energy. \n\n**Customisable Tool Features:**\n- Load Operating Characteristics (Min stable load, ramp rates, etc.)\n- Multiple Power Purchase Agreements (contract volume, strike, floor, etc.)\n\n**Features Coming Soon:**\n- Renewable Energy Certificate procurement + surrender (with/without temporal matching)\n- Shadow Pricing of Grid Emissions Intensity (average & marginal emissions)\n- Constrain to Green Energy Certification Standards for H2 (max tCO2 content per tH2) \n\n**Project Links**\n- Project Homepage: https://www.nemglo.org/\n- Python Github Repository: https://github.com/dec-heim/NEMGLO\n- Python Documentation: https://nemglo.readthedocs.io/en/latest/about.html\n- NEMGLO App Github Repository: https://github.com/dec-heim/NEMGLO-app\n\n\n## Installation\n```bash\npip install nemglo\n```\nFor guidance on installation and usage of [NEMGLO-app](https://github.com/dec-heim/NEMGLO-app) (a graphical user interface), please refer to its project page.\n\n## Usage\nFor guidance on `NEMGLO` usage, see the [Examples]() section of the documentation.\n\n## Contributing\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md).\nPlease note that this project is released with a [Code of Conduct](). By contributing to this project, you agree to abide by its terms.\n\n## License\n`NEMGLO` was created by Declan Heim as a Master\'s Project at UNSW. It is licensed under the terms of the [BSD 3-Clause license](LICENSE).\n\n## Credits\nThe `NEMGLO` project is affilitated with the [UNSW Collaboration on Energy and Environmental Markets](https://www.ceem.unsw.edu.au/). The [`NEMGLO-app`](https://github.com/dec-heim/NEMGLO-app) was financially supported by the [UNSW Digital Grid Futures Institute](https://www.dgfi.unsw.edu.au/) to Dec-2022.\n\n`NEMGLO` incorporates functionality from a suite of UNSW-CEEM tools, namely, [`NEMOSIS`](https://github.com/UNSW-CEEM/NEMOSIS) to extract historical market data and [`NEMED`](https://github.com/UNSW-CEEM/NEMED) to compute emissions data from AEMO\'s MMS databases respectively. The structure of the optimiser codebase is further adopted from sister tool [`nempy`](https://github.com/UNSW-CEEM/nempy) under [nempy licence](https://github.com/UNSW-CEEM/nempy/blob/master/LICENSE).\n\n### Acknowlgements\n\nMany thanks to:\n- Jay Anand, co-developer of `NEMGLO-app`. \n- Nick Gorman, Abhijith Prakash, and Shayan Naderi for pointers on `NEMGLO` code development (including adopted NEM tools).\n- Iain MacGill, Anna Bruce, Rahman Daiyan, and Jack Sheppard for advice at various stages to this project.\n\n## Contact\nQuestions and feedback are very much welcomed. Please reach out by email to [declanheim@outlook.com](mailto:declanheim@outlook.com)',
    'author': 'dec-heim',
    'author_email': '92137442+dec-heim@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
