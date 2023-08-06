# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttrontesting', 'volttrontesting.fixtures']

package_data = \
{'': ['*']}

install_requires = \
['anypubsub>=0.6,<0.7',
 'grequests>=0.6.0,<0.7.0',
 'mock>=4.0.3,<5.0.0',
 'pytest>=6.2.5,<7.0.0',
 'volttron>=10.0.2rc0,<11.0']

setup_kwargs = {
    'name': 'volttron-testing',
    'version': '0.4.0rc1',
    'description': 'The volttron-testing library contains classes and utilities for interacting with a VOLTTRON instance.',
    'long_description': '# volttron-testing\n\n[![Run Pytests](https://github.com/eclipse-volttron/volttron-testing/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-testing/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-testing.svg)](https://pypi.org/project/volttron-testing/)\n\nThe volttron-testing library contains classes and utilities for interacting with a VOLTTRON instance.\n\n## Prerequisites\n\n* Python >= 3.8\n\n## Installation\n\nCreate a virtual environment\n\n```shell \npython -m venv env\n```\n\nActivate the environment\n\n```shell\nsource env/bin/activate\n```\n\nInstall volttron-testing\n\n```shell\n# Installs volttron and volttron-testing\npip install volttron-testing\n```\n\n## Developing with TestServer\n\nThe following code snippet shows how to utilize the TestServer\'s internal pubsub to be able to test\nwith it outside of the volttron platform.\n\n```python\ndef test_send_alert():\n    """ Test that an agent can send an alert through the pubsub message bus."""\n    \n    # Create an agent to run the test with\n    agent = Agent(identity=\'test-health\')\n\n    # Create the server and connect the agent with the server\n    ts = TestServer()\n    ts.connect_agent(agent=agent)\n\n    # The health.send_alert should send a pubsub message through the message bus\n    agent.vip.health.send_alert("my_alert", Status.build(STATUS_BAD, "no context"))\n    \n    # We know that there should only be a single message sent through the bus and\n    # the specifications of the message to test against.\n    messages = ts.get_published_messages()\n    assert len(messages) == 1\n    headers = messages[0].headers\n    message = json.loads(messages[0].message)\n    assert headers[\'alert_key\'] == \'my_alert\'\n    assert message[\'context\'] == \'no context\'\n    assert message[\'status\'] == \'BAD\'\n\n```\n\nReference the volttrontesting package from within your environment in order to build tests against the TestServer.\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'VOLTTRON Team',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-testing',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
