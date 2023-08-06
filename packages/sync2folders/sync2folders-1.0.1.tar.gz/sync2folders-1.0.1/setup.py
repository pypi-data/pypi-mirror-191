# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync2folders']

package_data = \
{'': ['*']}

install_requires = \
['markdown>=3.3.4']

entry_points = \
{'console_scripts': ['sync2folders = sync2folders.__main__:main']}

setup_kwargs = {
    'name': 'sync2folders',
    'version': '1.0.1',
    'description': 'Synchronizes source and replica folders',
    'long_description': '<a src=\'https://www.rplumber.io/\'><img src=\'logo.png\' align="right" height="138.5" style="margin:10px;" /></a>\n\n![software-version](https://custom-icon-badges.demolab.com/badge/Version-v1.0.1-gray.svg?labelColor=informational&logo=stack) \n![software-state](https://custom-icon-badges.demolab.com/badge/Status%20-Under%20Development-gray.svg?labelColor=informational&logo=gear) \n[![PyPI version](https://badge.fury.io/py/sync2folders.svg)](https://badge.fury.io/py/sync2folders)\n\n![software-owner](https://custom-icon-badges.demolab.com/badge/Owner%20-Ivan%20Santos-gray.svg?labelColor=informational&logo=person)\n<a href="mailto:ivan@atlasmga.com" rel="nofollow">![owner-contact: ivan@atlasmga.com](https://custom-icon-badges.demolab.com/badge/Contact%20-ivan@atlasmga.com-gray.svg?labelColor=informational&logo=mail)</a>\n<br>\n<h1 style="text-align: left;">sync<span style="color: #00b336">2</span>folders</h1>\n\n<p style="text-align: justify;">This is a simple program that synchronizes two folders: source and replica. The program maintains a full, identical copy of source folder at replica folder. The program is written in Python.</p>\n\n<p style="text-align: justify;">The program is designed to be run from the command line. It takes four arguments: source folder path, replica folder path, synchronization interval and logs path. The program synchronizes the folders every time the interval expires. The program logs file creation/copying/removal operations to a file and to the console output.</p>\n\n<br>\n\n## **Features**\n\n- [x] Synchronization is one-way: after the synchronization content of the replica folder is modified to exactly match content of the source folder;\n- [x] Synchronization is performed periodically;\n- [x] File creation/copying/removal operations are logged to a file and to the console output;\n- [x] Folder paths, synchronization interval and log file path are provided using the command line arguments;\n\n<br>\n\n## **Quick Start**\n\n## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Get The Script From Git Hub Repo**\n\nInside a folder of your choice, clone the repository from command line:\n\n```bash\ngit clone https://github.com/ivanSantos16/sync2folders\n```\n\nYou can run the program from the command line and ask for help with the script variables:\n\n```bash\npython sync2folders -h                                                                             \n\nusage: synchronisation.py [-h] -s SOURCE -r REPLICA -p PERIOD -l LOGS\n\nSynchronizes two folders: source and replica\n\noptions:\n  -h, --help            show this help message and exit\n  -s SOURCE, --source SOURCE\n                        Source folder path\n  -r REPLICA, --replica REPLICA\n                        Replica folder path\n  -p PERIOD, --period PERIOD\n                        Period of time in seconds between each synchronization\n  -l LOGS, --logs LOGS  Logs file path\n```\n\n<br>\n\n### Arguments Description\n- `source` : Source folder path (required) [string]\n- `replica` : Replica folder path (required) [string]\n- `period` : Period of time in seconds between each synchronization (required) [int]\n- `logs` : Logs file path (required) [string]\n\n<br>\n\n### Different examples of running the program.\n\nFirst example:\n\n```bash\npython sync2folders -s <source_folder_path> -r <replica_folder_path> -p <sync_interval> -l <log_file_path>\n```\n\n```bash\npython sync2folders -s source -r replica -p 10 -l logs/logs.txt\n```\n<br>\n\nSecond example:\n\n```bash\npython sync2folders --source <source_folder_path> --replica <replica_folder_path> --period <sync_interval> --logs <log_file_path>\n```\n\n```bash\npython sync2folders --source source --replica replica --period 10 --logs logs/logs.txt\n```\n\n## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Get The Script From Pypi**\n\nFrom command line, install the package with pip:\n\n```bash\npython -m pip install sync2folders\n```\n\nFrom anywhere, you can run the program from the command line and ask for help with the script variables:\n\n```bash\npython -m sync2folders -h                                                 \n\nusage: synchronisation.py [-h] -s SOURCE -r REPLICA -p PERIOD -l LOGS\n\nSynchronizes two folders: source and replica\n\noptions:\n  -h, --help            show this help message and exit\n  -s SOURCE, --source SOURCE\n                        Source folder path\n  -r REPLICA, --replica REPLICA\n                        Replica folder path\n  -p PERIOD, --period PERIOD\n                        Period of time in seconds between each synchronization\n  -l LOGS, --logs LOGS  Logs file path\n```\n\n<br>\n\n### Arguments Description\n- `source` : Source folder path (required) [string]\n- `replica` : Replica folder path (required) [string]\n- `period` : Period of time in seconds between each synchronization (required) [int]\n- `logs` : Logs file path (required) [string]\n\n<br>\n\n### Different examples of running the program.\n\nFirst example:\n\n```bash\npython -m sync2folders -s <source_folder_path> -r <replica_folder_path> -p <sync_interval> -l <log_file_path>\n```\n\n```bash\npython -m sync2folders -s source -r replica -p 10 -l logs/logs.txt\n```\n<br>\n\nSecond example:\n\n```bash\npython -m sync2folders --source <source_folder_path> --replica <replica_folder_path> --period <sync_interval> --logs <log_file_path>\n```\n\n```bash\npython -m sync2folders --source source --replica replica --period 10 --logs logs/logs.txt\n```\n',
    'author': 'ivanSantos16',
    'author_email': 'ivan.rafa.16@gmail.com',
    'maintainer': 'ivanSantos16',
    'maintainer_email': 'ivan.rafa.16@gmail.com',
    'url': 'https://github.com/ivanSantos16/sync2folders',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
