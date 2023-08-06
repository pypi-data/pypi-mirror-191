# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_framework_mixins']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1,<5.0', 'djangorestframework']

entry_points = \
{'console_scripts': ['gen = rest_framework_mixins.generate:main']}

setup_kwargs = {
    'name': 'rest-framework-mixins',
    'version': '0.1.2',
    'description': 'A collection of DRF mixins combinations',
    'long_description': '# rest-framework-mixins\n\n## Installation\n\n`pip install rest_framework_mixins`\n\n## Usage\n\nThis package provides all combinations of the mixins provided by rest_framework.  \nAll combinations follow the same format: `{initials}Mixin.\n\nThe initials correspond to the following methods, in this specific order:\n\n- L: `list()`  \n- R: `retrieve()`  \n- C: `create()`  \n- U: `update()`  \n- P: `partial_update()`  \n- D: `delete()`  \n\nSo for example, to import a mixin that gives us list, retrieve and create,\nwe can do the following:\n\n```\nfrom rest_framework_mixins import LRCMixin\n\nclass CreateListRetrieveViewSet(LRCMixin, viewsets.GenericViewSet):\n    """\n    A viewset that provides `retrieve`, `create`, and `list` actions.\n\n    To use it, override the class and set the `.queryset` and\n    `.serializer_class` attributes.\n    """\n    pass\n```\n\n> Adapted from [DRF\'s documentation](https://www.django-rest-framework.org/api-guide/viewsets/#example_3)\n',
    'author': 'Xavier Francisco',
    'author_email': 'xavier.n.francisco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Qu4tro/rest_framework_mixins',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
