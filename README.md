NXSC
====
*Copyright &copy; 2013 Michał "NeoXant" Kolarczyk*  
This software is under GNU General Public License version 3.  
Content of license is in the file LICENSE.md or at http://www.gnu.org/licenses/gpl.html

***

NXSC is a Python script for easy download, install and update software on Microsoft Windows  
This script is similar to `apt-get` or `aptitude` in Debian/Ubuntu.

NXSC uses [FileHippo.com](http://filehippo.com/) to search and install software.  
Custom repositories will be available in future versions.  

**List of all functions (links lead to the corresponding page on the wiki):**
- [search](https://github.com/NeoXant/nxsc/wiki/Search)
- [install](https://github.com/NeoXant/nxsc/wiki/Install) (for now without unattended installation)
- [upgrade](https://github.com/NeoXant/nxsc/wiki/Upgrade)
- [display](https://github.com/NeoXant/nxsc/wiki/Show) additional information about package

**Requirements for using pure Python script:**
- [Python](http://python.org/) 3.3
- [Requests](http://docs.python-requests.org/en/latest/)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
- [PyYAML](http://pyyaml.org/)
- [python-progressbar](https://code.google.com/p/python-progressbar/) (in PyPI: progressbar-latest)
- [hurry.filesize](https://pypi.python.org/pypi/hurry.filesize)

**How to run:**    
Usage for 0.1.0 version:
```
usage: nxsc.py [-h] [--version] {install,search,update,upgrade,show,download} ...

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
#### Changelog ####

| Version | Publish date | Changes | Binary version (setup file) | Pure Python script |
|:-------:|:------------:|---------|-----------------------------|--------------------|
| 0.1.0 | 2013-06-24 | First version | [nxsc-0.1.0-setup.exe](http://adf.ly/4156858/nxsc-010-setup) | [ver-0.1.0](https://github.com/NeoXant/nxsc/archive/ver-0.1.0.zip) |
| 0.1.1 | 2013-06-25 | Bug: KeyError: 'new version' | [nxsc-0.1.1-setup.exe](http://adf.ly/4156858/nxsc-011-setup) | [ver-0.1.1](https://github.com/NeoXant/nxsc/archive/ver-0.1.1.zip)|
| 0.1.2 | 2013-06-26 | Fixes #1 | [nxsc-0.1.2-setup.exe](http://adf.ly/R8zCO) | [ver-0.1.2](http://adf.ly/R8zK9) |

#### Difference between a binary version and pure Python script ####
With binary version, you don't need to have Python interpreter (and other libraries) installed on your machine because it have all this built-in.
