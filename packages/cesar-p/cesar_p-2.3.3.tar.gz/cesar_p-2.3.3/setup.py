# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cesarp',
 'cesarp.SIA2024',
 'cesarp.SIA2024.demand_generators',
 'cesarp.common',
 'cesarp.common.profiles',
 'cesarp.common.typing',
 'cesarp.construction',
 'cesarp.emissons_cost',
 'cesarp.energy_strategy',
 'cesarp.eplus_adapter',
 'cesarp.geometry',
 'cesarp.graphdb_access',
 'cesarp.manager',
 'cesarp.model',
 'cesarp.operation',
 'cesarp.operation.fixed',
 'cesarp.results',
 'cesarp.retrofit',
 'cesarp.retrofit.all_bldgs',
 'cesarp.retrofit.embodied',
 'cesarp.retrofit.energy_perspective_2050',
 'cesarp.site',
 'cesarp.weather',
 'cesarp.weather.swiss_communities',
 'cesarp.weather.swiss_communities.ressources']

package_data = \
{'': ['*'],
 'cesarp.SIA2024': ['generated_params/nominal/*',
                    'generated_params/variable/*'],
 'cesarp.energy_strategy': ['ressources/business_as_usual/efficiencies/*',
                            'ressources/business_as_usual/energymix/*',
                            'ressources/business_as_usual/fuel/*',
                            'ressources/business_as_usual/retrofit/*',
                            'ressources/general/*',
                            'ressources/new_energy_policy/efficiencies/*',
                            'ressources/new_energy_policy/energymix/*',
                            'ressources/new_energy_policy/fuel/*',
                            'ressources/new_energy_policy/retrofit/*'],
 'cesarp.eplus_adapter': ['ressources/*'],
 'cesarp.graphdb_access': ['ressources/*'],
 'cesarp.operation.fixed': ['ressources/*'],
 'cesarp.retrofit.embodied': ['ressources/*'],
 'cesarp.retrofit.energy_perspective_2050': ['ressources/*'],
 'cesarp.weather.swiss_communities.ressources': ['weather_files/*']}

install_requires = \
['PyYaml>=5.4,<6.0',
 'SPARQLWrapper>=1.8,<2.0',
 'Shapely>=1.7,<2.0',
 'eppy>=0.5,<0.6',
 'esoreader>=1.2,<2.0',
 'jsonpickle>=2.0.0,<3.0.0',
 'numpy>=1.20,<2.0',
 'openpyxl>=3.0,<4.0',
 'pandas>=1.3,<2.0',
 'pint>=0.17,<0.18',
 'python-contracts>=0.1,<0.2',
 'rdflib>=6.0,<7.0',
 'requests>=2.26.0,<3.0.0',
 'scipy>=1.7,<2.0',
 'types-PyYAML>=5.4.3,<6.0.0',
 'types-requests>=2.26.2,<3.0.0',
 'types-six>=0.1.7,<0.2.0']

extras_require = \
{'geomeppy': ['geomeppy>=0.11,<0.12'],
 'geopandas': ['geopandas>=0.9.0,<0.10.0']}

setup_kwargs = {
    'name': 'cesar-p',
    'version': '2.3.3',
    'description': 'Combined Energy Simulation And Retrofit',
    'long_description': '**CESAR-P** stands for **C**ombined **E**nergy **S**imulation **A**nd **R**etrofit in **P**yhton.\n\nThe package allows for simulating the building **energy demand of a district**, including options for retrofitting, cost and emission calculation. The energy demand simulated includes:\n\n- heating\n- domestic hot water\n- cooling\n- electricity\n\nThe tool was developed at **Urban Energy Systems Lab**, which is part of the Swiss Federal Laboratories for Materials Science and Technology (Empa).\n\n**Usage examples** can be found under https://github.com/hues-platform/cesar-p-usage-examples\n\nFor more details please have a look at the documentation, linked in the side menu. A good starting point for general information is the **README** section. It includes a detailed **installation guide**.\n',
    'author': 'Urban Energy Systems Lab - Empa',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hues-platform/cesar-p-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
