# CTFd Interface 2 (ctfi2)
## Table of Contents
- [CTFd Command Line Interface 2 (ctfcli2)](#CTFd-Command-Line-Interface-2-ctfcli2)
    - [Description](#description)
    - [Change Log](#change-log)
    - [Limitations](#limitations)
    - [Installation](#installation)
        - [Requirements](#requirements)
        - [Linux](#linux)

### Description
ctfi2 is a management tool for [CTFd](https://github.com/CTFd/CTFd) Server instance(s).

Key Features:
* Handsome Graphical User Interface!
* Granular control of your Challenges and Users
* At-a-glance view of all Challenges
* Manage multiple CTFd instances simultaneously

### Change Log
- Version 1.0 (Acceptable Axolotl)
    - Initial Release

- TODO:
    - Reduce the volume of tastey spaghetti!
    - Inuitive, msfconsole-esq, Command Line Mode
    - Import/Export of configuration data

### Limitations
* The system is unable to init, reset or wipe an existsing CTFd instance at this time.

### Installation
ctfi2 has been tested on:
* Ubuntu 20.04 LTS
* Debian Buster

##### Requirements
* [Python >= 3.6 (64-bit) ](https://www.python.org/downloads/release/python-360/)
* [Requests >= 2.22.0](https://requests.readthedocs.io/en/master/)
* [PyQt5 >= 5.9.2](https://pypi.org/project/PyQt5/)

##### Linux
Clone the repo 
```  
git clone https://github.com/drpresq/ctfcli2
```
Install using setuptools
```
pip3 install -r ./ctfi2/requirements.txt 
pip3 install ./ctfi2
```

Run it!:
```
ctfi2
```

(Optional) Run it without installation:
```
./ctfi2/src/ctfi2.py
```


