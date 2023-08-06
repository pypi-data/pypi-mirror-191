# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_logging']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>1.4', 'np_config>0.4.12']

setup_kwargs = {
    'name': 'np-logging',
    'version': '0.3.8',
    'description': 'Pre-configured file, web, and email logging for Mindscope neuropixels projects, repackaging code from AIBS mpeconfig.',
    'long_description': "# **np_logging**\n\n***\n\n**For use on internal Allen Institute network**\n\n***\n\n\n## Quick start\n\nFollow the conventions for using the `logging` module in the standard library:\n\n - in a script or main module, `np_logging` adds console & file handlers and exit messages to the root logger:\n\n```python\nimport np_logging\n\nlogger = np_logging.getLogger()\n```\n\n\n - or, in a package or project with multiple modules, all logged messages are propagated to the root logger:\n```python\nimport np_logging\n\nlogger = np_logging.getLogger(__name__)     # logger.level = logging.NOTSET = 0\n```\n\n\n - then log messages as usual:\n\n```python \nlogger.info('test message')\nlogger.warning('test message')\n```\n\n\nNo further setup is required, and importing `logging`\nfrom the standard library isn't necessary.\n\n\n***\n\n\nTo send a message to the Mindscope log-server, use `np_logging.web()` and supply a project name, which will\nappear in the \n`channel` field on the server:\n\n```python\nproject_name = 'spike_sorting'\n\nnp_logging.web(project_name).info('test message')\n```\n- the web log can be viewed at [http://eng-mindscope:8080](http://eng-mindscope:8080)\n\n***\n\n\nFor customization, use `np_logging.setup()` to supply a logging config dict than specifies\nloggers and their handlers/formatters, and extra functions such as exit messages & exit\nemails will be added.\n\n- logging configs should be specified according to the python logging [library dict schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)\n\n\n- logging configs on the `eng-mindscope` ZooKeeper server can also be used directly to setup\n  logging by supplying their path to `np_logging.setup()`:\n\n```python\nnp_logging.setup(\n    '/projects/np_workflows/defaults/logging'\n)\n```\n\nSee [np_config](https://github.com/AllenInstitute/np_config) for further info on using ZooKeeper\nfor configs.\n\n\n\nOther input arguments to `np_logging.setup()`:\n\n- `project_name` (default: current working directory name) \n  \n    - sets the `channel` displayed on the log server\n\n- `email_address` (default: `None`)\n      \n    - if one or more addresses are supplied, an email is sent at program exit reporting the\n      elapsed time and cause of termination. If an exception was raised, the\n      traceback is included.\n\n- `log_at_exit` (default: `True`)\n\n    - If `True`, a message is logged when the program terminates, reporting total\n      elapsed time.\n\n- `email_at_exit` (default: `False`, or `True` if `email_address` is not `None`)\n\n    - If `True`, an email is sent when the program terminates.\n      \n    - If `logging.ERROR`, the email is only sent if the program terminates via an exception.\n\n",
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben Hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
