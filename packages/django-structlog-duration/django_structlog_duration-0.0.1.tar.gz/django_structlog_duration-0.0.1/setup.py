# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_structlog_duration']

package_data = \
{'': ['*']}

install_requires = \
['django-structlog>=4,<5']

setup_kwargs = {
    'name': 'django-structlog-duration',
    'version': '0.0.1',
    'description': 'Add request duration to django-structlog request log.',
    'long_description': '# django-structlog-duration\n\nIf you use [django-structlog](https://github.com/jrobichaud/django-structlog), this is a little extension that will populate the `request_finished` log with the duration of the request (`request_duration`).\n\n## Installation\n\nInstall the package.\n\n```sh\npip install django-structlog-duration\n```\n\nConfigure the middleware.\n\n```python\nMIDDLEWARE = [\n    "django_structlog_duration.StartTimer",\n    # ...\n    "django_structlog.middlewares.RequestMiddleware",\n    "django_structlog_duration.StopTimer",\n]\n```',
    'author': 'Tomasz Knapik',
    'author_email': 'tomasz@knapik.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tm-kn/django-structlog-duration',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
