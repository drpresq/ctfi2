# CTFd Interface 2 (ctfi2)
## Table of Contents
- [CTFd Interface 2 (ctfi2)](#CTFd-Interface-2-ctfi2)
    - [Description](#description)
    - [Change Log](#change-log)
    - [Limitations](#limitations)
    - [Installation](#installation)
        - [Requirements](#requirements)
        - [Cross-platform From PIP](#cross-platform-from-pip)
	- [Linux From Source](#linux-from-source)

### Description
ctfi2 is a management tool for [CTFd](https://github.com/CTFd/CTFd) Server instance(s).

Key Features:
* Handsome Graphical User Interface!
* Add and Remove configuration objects (Users, Challenges, Flags, Hints, Files) in real time.
* Import Users from CSV or bulk create generic ones.
* Manage multiple _independent_ CTFd instances simultaneously

### Change Log
- Version 1.5.4 (Acceptable Axolotl)
    - **New** Published package to pypi.org for easy pip installation
    - **Update** README.md

- Version 1.5 (Acceptable Axolotl)
    - **New** Server Level Functionality: Initialize, Reset and Wipe CTFd Instances!
    - **New** ["Documentation"](docs/main.md)
    - **Update** Readme
    - **Update** Squished a bug in the file handler that saved challenge files to funky paths
    
- Version 1.0 (Acceptable Axolotl)
    - Initial Release

- TODO:
    - [X] Documentation
    - [X] Reduce the volume of tastey spaghetti!
    - [ ] Inuitive, msfconsole-esq, Command Line Mode
    - [ ] Import/Export of configuration data

### Limitations
* ~~The system is unable to init, reset or wipe an existsing CTFd instance at this time.~~ (Fixed as of v1.5)

### Installation
ctfi2 has been tested on:
* Ubuntu 20.04 LTS
* Debian Buster

##### Requirements
* [Python >= 3.6 (64-bit)](https://www.python.org/downloads/release/python-360/)
* [Requests >= 2.22.0](https://requests.readthedocs.io/en/master/)
* [PyQt5 >= 5.9.2](https://pypi.org/project/PyQt5/)

##### Cross-Platform From PIP

```
pip3 install ctfi2
```

##### Linux From Source
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


