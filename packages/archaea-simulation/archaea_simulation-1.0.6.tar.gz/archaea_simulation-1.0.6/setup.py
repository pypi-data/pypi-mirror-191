# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['archaea_simulation', 'archaea_simulation.simulation_objects']

package_data = \
{'': ['*']}

install_requires = \
['archaea>=1.1.13,<2.0.0']

setup_kwargs = {
    'name': 'archaea-simulation',
    'version': '1.0.6',
    'description': 'Wrapper definitions for simulation tools.',
    'long_description': "# Archaea Simulation\n\nWrapper definitions for simulation tools.\n\nMotivation of creating this library is started with master thesis, departments of Computational\nScience and Engineering and Architecture at Istanbul Technical University. \nAim of thesis is to create scenarios for different environmental\nsolvers like EnergyPlus and OpenFOAM to run them parallely on Linux environment.\nPreparation of these scenario files done by geometric [Archaea](https://github.com/archaeans/archaea) library.\n\n\n## Focused Simulation Tools\n\n- OpenFOAM: OpenFOAM requires stl geometries to run it's solvers\nbehind the scenes. (Pre-Alpha)\n- EnergyPlus: EnergyPlus requires idf schema to run simulations. (MVP)\n- UWG: Urban weather generator is a solver to calculate effects on urban microclimate.\nIt creates new .epw file for EnergyPlus simulations.\n\nMain idea behind this work is to be experimental and didactic. ",
    'author': 'Oğuzhan Koral',
    'author_email': 'oguzhankoral@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/archaeans/archaea-simulation',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
