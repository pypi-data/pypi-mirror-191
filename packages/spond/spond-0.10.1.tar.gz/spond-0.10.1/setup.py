# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spond']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'spond',
    'version': '0.10.1',
    'description': 'Simple, unofficial library with some example scripts to access data from the Spond API.',
    'long_description': "# Spond\n![spond logo](https://github.com/Olen/Spond/blob/main/images/spond-logo.png?raw=true)\n\nSimple, unofficial library with some example scripts to access data from the [Spond](https://spond.com/) API.\n\n## Install\n\n`pip install spond`\n\n## Usage\n\nYou need a username and password from Spond\n\n\n\n### Example code\n\n```\nimport asyncio\nfrom spond import spond\n\nusername = 'my@mail.invalid'\npassword = 'Pa55worD'\ngroup_id = 'C9DC791FFE63D7914D6952BE10D97B46'  # fake \n\nasync def main():\n    s = spond.Spond(username=username, password=password)\n    group = await s.get_group(group_id)\n    print(group['name'])\n    await s.clientsession.close()\n\nasyncio.run(main())\n\n```\n\n## Key methods\n\n### get_groups()\n\nGet details of all your group memberships and all members of those groups.\n\n### get_events([group_id, include_scheduled, max_end, min_end, max_start, min_start, max_events])\n\nGet details of events, limited to 100 by default.\nOptional parameters allow filtering by start and end datetimes, group; more events to be returned; inclusion of 'scheduled' events.\n\n### get_person()\nGet a member's details.\n\n### get_messages()\nGet all your messages.\n\n### send_message(chat_id, text)\nSend a message with content `text` in a specific chat with id `chat_id`.\n\n## Example scripts\n\nThe following scripts are included as examples.  Some of the scripts might require additional packages to be installed (csv, ical etc).\n\nRename the file `config.py.sample` to `config.py` and add your username and password to the file before running the samples.\n\n### ical.py\nGenerates an ics-file of upcoming events.\n\n### groups.py\nGenerates a json-file for each group you are a member of.\n\n### attendance.py &lt;-f from_date&gt; &lt;-t to_date&gt; [-a]\nGenerates a csv-file for each event between `from_date` and `to_date` with attendance status of all organizers.  The optional parameter `-a` also includes all members that has been invited.\n\n## AsyncIO\n[Asyncio](https://docs.python.org/3/library/asyncio.html) might seem intimidating in the beginning, but for basic stuff, it is quite easy to follow the examples above, and just remeber to prefix functions that use the API with `async def ...` and to `await` all API-calls and all calls to said functions.\n\n[This article](https://realpython.com/async-io-python/) will give a nice introduction to both why, when and how to use asyncio in projects.\n\n",
    'author': 'Ola Thoresen',
    'author_email': 'ola@nytt.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Olen/Spond',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
