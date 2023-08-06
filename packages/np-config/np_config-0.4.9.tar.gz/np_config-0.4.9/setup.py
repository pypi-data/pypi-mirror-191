# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_config']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.0,<2.0',
 'kazoo>=2.8,<2.9',
 'pyyaml>=5.3.0,<6.0.0',
 'requests',
 'types-PyYaml',
 'typing-extensions']

extras_require = \
{'dev': ['pip-tools', 'isort', 'mypy', 'black', 'pytest', 'poetry']}

setup_kwargs = {
    'name': 'np-config',
    'version': '0.4.9',
    'description': 'Zookeeper configs with local backup, repackaging code from AIBS mpeconfig.',
    'long_description': "**For use on internal Allen Institute network**\n\n- fetch configs from ZooKeeper or .yaml/.json file via their path:\n```python\ntest_config: dict = np_config.fetch(\n    '/projects/np_logging_test/defaults/logging'\n)\n```\n\n- the Mindscope ZooKeeper server is at `eng-mindscope:2181`\n- configs can be added via ZooNavigator webview:\n  [http://eng-mindscope:8081](http://eng-mindscope:8081)\n- or more conveniently, via an extension for VSCode such as [gaoliang.visual-zookeeper](https://marketplace.visualstudio.com/items?itemName=gaoliang.visual-zookeeper)\n\n- configs are cached locally: if the ZooKeeper server is unavailable, the local copy will be used",
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben Hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
