# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['highlight_io', 'highlight_io.integrations']

package_data = \
{'': ['*']}

install_requires = \
['opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-distro[otlp]>=0.36b0,<0.37',
 'opentelemetry-exporter-otlp-proto-http>=1.15.0,<2.0.0',
 'opentelemetry-instrumentation-logging>=0.36b0,<0.37',
 'opentelemetry-instrumentation>=0.36b0,<0.37',
 'opentelemetry-proto>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0']

extras_require = \
{'azure': ['azure-functions>=1.13.2,<2.0.0'],
 'flask': ['blinker>=1.5,<2.0', 'flask>=2.2.2,<3.0.0']}

setup_kwargs = {
    'name': 'highlight-io',
    'version': '0.1.7',
    'description': 'Session replay and error monitoring: stop guessing why bugs happen!',
    'long_description': '',
    'author': 'Vadim Korolik',
    'author_email': 'vadim@highlight.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.highlight.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
