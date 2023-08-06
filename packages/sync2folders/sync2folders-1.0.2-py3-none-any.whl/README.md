<a src='https://www.rplumber.io/'><img src='logo.png' align="right" height="138.5" style="margin:10px;" /></a>

![software-version](https://custom-icon-badges.demolab.com/badge/Version-v1.0.2-gray.svg?labelColor=informational&logo=stack) 
![software-state](https://custom-icon-badges.demolab.com/badge/Status%20-Under%20Development-gray.svg?labelColor=informational&logo=gear) 
[![PyPI version](https://badge.fury.io/py/sync2folders.svg)](https://badge.fury.io/py/sync2folders)

![software-owner](https://custom-icon-badges.demolab.com/badge/Owner%20-Ivan%20Santos-gray.svg?labelColor=informational&logo=person)
<a href="mailto:ivan.rafa.16@gmail.com" rel="nofollow">![owner-contact: ivan.rafa.16@gmail.com](https://custom-icon-badges.demolab.com/badge/Contact%20-ivan.rafa.16@gmail.com-gray.svg?labelColor=informational&logo=mail)</a>
<br>
<h1 style="text-align: left;">sync<span style="color: #00b336">$\color[rgb]{0,0.67,0.2} 2$</span>folders</h1>

<p style="text-align: justify;">This is a simple program that synchronizes two folders: source and replica. The program maintains a full, identical copy of source folder at replica folder. The program is written in Python.</p>

<p style="text-align: justify;">The program is designed to be run from the command line. It takes four arguments: source folder path, replica folder path, synchronization interval and logs path. The program synchronizes the folders every time the interval expires. The program logs file creation/copying/removal operations to a file and to the console output.</p>

<br>

## **Features**

- [x] Synchronization is one-way: after the synchronization content of the replica folder is modified to exactly match content of the source folder;
- [x] Synchronization is performed periodically;
- [x] File creation/copying/removal operations are logged to a file and to the console output;
- [x] Folder paths, synchronization interval and log file path are provided using the command line arguments;

<br>

## **Quick Start**
<details>
  <summary><h2><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get The Script From Git Hub Repo</strong></h2></summary>

Inside a folder of your choice, clone the repository from command line:

```bash
git clone https://github.com/ivanSantos16/sync2folders
```

You can run the program from the command line and ask for help with the script variables:

```bash
python sync2folders -h                                                                             

usage: synchronisation.py [-h] -s SOURCE -r REPLICA -p PERIOD -l LOGS

Synchronizes two folders: source and replica

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Source folder path
  -r REPLICA, --replica REPLICA
                        Replica folder path
  -p PERIOD, --period PERIOD
                        Period of time in seconds between each synchronization
  -l LOGS, --logs LOGS  Logs file path
```

<br>

### Arguments Description
- `source` : Source folder path (required) [string]
- `replica` : Replica folder path (required) [string]
- `period` : Period of time in seconds between each synchronization (required) [int]
- `logs` : Logs file path (required) [string]

<br>

### Different examples of running the program.

First example:

```bash
python sync2folders -s <source_folder_path> -r <replica_folder_path> -p <sync_interval> -l <log_file_path>
```

```bash
python sync2folders -s source -r replica -p 10 -l logs/logs.txt
```
<br>

Second example:

```bash
python sync2folders --source <source_folder_path> --replica <replica_folder_path> --period <sync_interval> --logs <log_file_path>
```

```bash
python sync2folders --source source --replica replica --period 10 --logs logs/logs.txt
```
</details>
  
<details open>
<summary><h2><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get The Script From Pypi</strong></h2></summary>


From command line, install the package with pip:

```bash
python -m pip install sync2folders
```

From anywhere, you can run the program from the command line and ask for help with the script variables:

```bash
python -m sync2folders -h                                                 

usage: synchronisation.py [-h] -s SOURCE -r REPLICA -p PERIOD -l LOGS

Synchronizes two folders: source and replica

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Source folder path
  -r REPLICA, --replica REPLICA
                        Replica folder path
  -p PERIOD, --period PERIOD
                        Period of time in seconds between each synchronization
  -l LOGS, --logs LOGS  Logs file path
```

<br>

### Arguments Description
- `source` : Source folder path (required) [string]
- `replica` : Replica folder path (required) [string]
- `period` : Period of time in seconds between each synchronization (required) [int]
- `logs` : Logs file path (required) [string]

<br>

### Different examples of running the program.

First example:

```bash
python -m sync2folders -s <source_folder_path> -r <replica_folder_path> -p <sync_interval> -l <log_file_path>
```

```bash
python -m sync2folders -s source -r replica -p 10 -l logs/logs.txt
```
<br>

Second example:

```bash
python -m sync2folders --source <source_folder_path> --replica <replica_folder_path> --period <sync_interval> --logs <log_file_path>
```

```bash
python -m sync2folders --source source --replica replica --period 10 --logs logs/logs.txt
```
</details open>
