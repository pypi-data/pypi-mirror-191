# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdh']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'humanize>=4.0.0,<5.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'pdpyras>=4.3.0,<5.0.0',
 'rich>=10.10.0,<11.0.0']

entry_points = \
{'console_scripts': ['pdh = pdh.main:main']}

setup_kwargs = {
    'name': 'pdh',
    'version': '0.3.6',
    'description': 'Pagerduty CLI for Humans',
    'long_description': '# PDH - PagerDuty CLI for humans\n\n![Build Image](https://github.com/mbovo/pdh/actions/workflows/build-image.yml/badge.svg)\n\n`PDH` is a new lightweight CLI for pagerduty interaction: uou can handle your incidents triage without leaving your terminal.\nIt also add some nice tricks to automate the incident triage and easy the on-call burden.\n\nSee [docs](./docs) (TBD)\n\n## Usage\n\nFirst of all you need to configure `pdh` to talk with PagerDuty\'s APIs:\n\n```bash\npdh config\n```\n\nThe wizard will prompt you for 3 settings:\n\n- `apikey` is the API key, you can generate it from the user\'s profile page on pagerduty website\n- `email` the email address of your pagerduty profile\n- `uid` the userID of your account (you can read it from the browser address bar when clicking on "My Profile")\n\nSettings are persisted to `~/.config/pdh.yaml` in clear.\n\n### Listing incidents\n\nAssigned to self:\n\n```bash\npdh inc ls\n```\n\nAny other incident currently outstanding:\n\n```bash\npdh inc ls -e\n```\n\n### Auto ACK incoming incidents\n\nWatch for new incidents every 10s and automatically set them to `Acknowledged`\n\n```bash\npdh inc ls --watch --new --ack --timeout 10\n```\n\n### List all HIGH priority incidents periodically\n\nList incidents asssigned to all users every 5s\n\n```bash\npdh inc ls --high --everything --watch --timeout 5\n```\n\n### Resolve specific incidents\n\n```bash\npdh inc resolve INCID0001 INCID0024 INCID0023\n```\n\n### Resolve all incidents related to `Backups`\n\n```bash\npdh inc ls --resolve --regexp ".*Backup.*"\n```\n\n## Rules\n\n`PDH` support custom scripting applied to your incidents list. These `rules` are in fact any type of executable you can run on your machine.\n\n```bash\npdh inc apply INCID001 -s /path/to/my/script.py -s /path/to/binary\n```\n\nThe `apply` subcommand will call the listed executable/script passing along a json to stdin with the incident informations. The called script can apply any type of checks/sideffects and output another json to stout to answer the call.\n\nEven though rules can be written in any language it\'s very straightforward using python:\n\n### Rules: an example\n\nAn example rule can be written in python with the following lines\n\n```python\n#!/usr/bin/env python3\nfrom pdh import rules, Filter\n\n@rules.rule\ndef main(input):\n    return {i["id"]: i["summary"] for i in input}\n\nif __name__ == "__main__":\n    main()\n```\n\nThis is the simplest rule you can write, reading the input and simply output a new dictionary with the entries. It will output something like:\n\n```bash\n\n pdh inc apply Q1LNI5LNM7RZ2C Q1C5KG41H0SZAM -s ./a.py\n┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ script ┃ Q1LNI5LNM7RZ2C                                                     ┃ Q1C5KG41H0SZAM                                                                       ┃\n┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ ./a.py │  AWS Health Event: us-east-1 EC2 : AWS_EC2_INSTANCE_STOP_SCHEDULED │  AWS Health Event: us-east-1 EC2 : AWS_EC2_INSTANCE_STORE_DRIVE_PERFORMANCE_DEGRADED │\n└────────┴────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘\n```\n\nThe default output is `table` with one line for each script runned and with one column per each element in the returned object\n\n### Rules: more examples\n\n```python\n#!/usr/bin/env python3\n\n# Needed imports\nfrom pdh import rules, Filter\n\n# This annotation make the main() method parse stdin as json into the parameter called input\n# All returned values are converted to json and printed to stdout\n@rules.rule\ndef main(input):\n\n    # Initialize PagerDuty\'s APIs\n    api = rules.api()\n\n    # From the given input extract only incidents with the word cassandra in title\n    incs = Filter.objects(input, filters=[Filter.regexp("title", ".*EC2.*")])\n\n    # ackwnoledge all previously filtered incidents\n    api.ack(incs)\n\n    # resolve all previously filtered incidents\n    api.resolve(incs)\n\n    # snooze all previously filtered incidents for 1h\n    api.snooze(incs, duration=3600)\n\n    # Chain a given rule, i.e call that rule with the output of this one\n    # chain-loading supports only a single binary, not directories\n    c = rules.chain(incs, "rules/test_chaining.sh")\n\n    # Execute an external program and get the output/err/return code\n    p: rules.ShellResponse = rules.exec(\'kubectl get nodes -o name\')\n    if p.rc > 0:\n      nodes = p.stdout.split("\\n")\n\n    # if you return a dict will be rendered with each item as a column in a table\n    # Othrwise will be converted as string\n    return {i["id"]: i["summary"] for i in incs}\n\n\nif __name__ == "__main__":\n    main()\n\n\n```\n\n## Requirements\n\n- [Taskfile](https://taskfile.dev)\n- Python >=3.9\n- Docker\n\n## Contributing\n\nFirst of all you need to setup the dev environment, using Taskfile:\n\n```bash\ntask setup\n```\n\nThis will create a python virtualenv and install `pre-commit` and `poetry` in your system if you lack them.\n',
    'author': 'Manuel Bovo',
    'author_email': 'manuel.bovo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mbovo/pdh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
