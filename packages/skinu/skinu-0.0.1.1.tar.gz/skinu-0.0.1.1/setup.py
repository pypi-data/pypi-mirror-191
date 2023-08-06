# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['skinu',
 'skinu._internal',
 'skinu.core',
 'skinu.performance',
 'skinu.sdms',
 'skinu.sdms.cb',
 'skinu.sdms.cb.est.performance_log',
 'skinu.sdms.cb.est.tag_est_log',
 'skinu.sdms.cb.message.master',
 'skinu.sdms.cb.message.skadi',
 'skinu.sdms.cb.raw.lab',
 'skinu.sdms.cb.raw.rst',
 'skinu.sdms.cb.raw_eai.skadi',
 'skinu.sdms.cb.ref.equip_ref',
 'skinu.sdms.cb.skadi.common',
 'skinu.sdms.cb.skadi.site',
 'skinu.sdms.cb.worklog.skadi',
 'skinu.utils']

package_data = \
{'': ['*']}

install_requires = \
['autopep8==2.0.1',
 'colorama==0.4.6',
 'colorlog>=6.7.0,<7.0.0',
 'couchbase>=4.1.2,<5.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pycodestyle>=2.10.0,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'six>=1.16.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'twine>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'skinu',
    'version': '0.0.1.1',
    'description': 'skadi support library package',
    'long_description': '# py-skinu\n\n',
    'author': 'JeongHun Lee',
    'author_email': 'None',
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
