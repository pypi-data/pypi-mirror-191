# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_iolanta', 'mkdocs_iolanta.cli']

package_data = \
{'': ['*'],
 'mkdocs_iolanta': ['_data/foaf/*',
                    '_data/iolanta/*',
                    '_data/octa/*',
                    '_data/owl/*',
                    '_data/rdf/*',
                    '_data/rdfs/*',
                    '_data/skos/*',
                    'data/*']}

install_requires = \
['iolanta-jinja2>=0.1.2,<0.2.0', 'mkdocs>=1.4.2,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['iolanta = mkdocs_iolanta.plugin:IolantaPlugin']}

setup_kwargs = {
    'name': 'mkdocs-iolanta',
    'version': '0.1.1',
    'description': 'MkDocs plugin to integrate with Iolanta semantic web framework.',
    'long_description': '',
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
