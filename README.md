NXSC
====
*Copyright &copy; 2013 Michał "NeoXant" Kolarczyk*  
This software is under GNU General Public License version 3.  
Content of license is in the file LICENSE.md or at http://www.gnu.org/licenses/gpl.html

***
**First verion of NXSC is not published yet! I created this README and wiki, because I want you to saw capability of this script and how to use it in the future.**

NXSC is a Python script for easy download, install and update software on Microsoft Windows operating systems  
This script is similar to `apt-get` or `aptitude` in Debian/Ubuntu.

NXSC uses [FileHippo.com](http://filehippo.com/) to search and install software.  
Custom repositories will be available in future versions.  

**List of all functions (links lead to the corresponding page on the wiki):**
- search
- install (for now without unattended installation)
- upgrade
- display additional information about package

**Requirements for using pure Python script:**
- [Python](http://python.org/) 3.3
- [Requests](http://docs.python-requests.org/en/latest/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [PyYAML](http://pyyaml.org/)

**How to run:**  
Shabang is set to `#!python3` so you don't need to add `python` or `python3` before `nxsc.py ...`.  
Usage for 0.1.0 version:
```
usage: nxsc [-h] [--version] {install,search,update,upgrade,show,download} ...

Python script for easy download, install and update software on Microsoft Windows

positional arguments:
  {install,search,update,upgrade,show,download}
                        commands to execute:
    install             install application(s)
    search              search for application(s)
    update              update information about installed applications
    upgrade             install updates
    show                displays detailed information about one or more applications
    download            only download application(s) without installing

optional arguments:
  -h, --help            show this help message and exit
  --version             show version

More information at http://github.com/NeoXant/nxsc
```
